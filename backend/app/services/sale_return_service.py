from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException, NotFoundException
from app.enums.transaction_type import TransactionType
from app.repositories.sale_item_repository import SaleItemRepository
from app.repositories.sale_return_repository import SaleReturnRepository
from app.schemas.inventory_transaction import InventoryTransactionCreate
from app.schemas.pagination import PaginatedResponse
from app.schemas.sale_return import SaleReturnCreate
from app.services.inventory_service import InventoryService


class SaleReturnService:

    def __init__(self):
        self.sale_return_repository = SaleReturnRepository()
        self.sale_item_repository = SaleItemRepository()
        self.inventory_service = InventoryService()

    def create(
        self,
        db: Session,
        sale_return: SaleReturnCreate,
    ):

        sale_item = self.sale_item_repository.get_by_id(
            db, sale_return.sale_item_id
        )

        if sale_item is None:
            raise NotFoundException("Sale item")

        already_returned = self.sale_return_repository.get_total_returned(
            db, sale_return.sale_item_id
        )

        remaining = sale_item.quantity - already_returned

        if sale_return.quantity > remaining:
            raise BadRequestException(
                f"Cannot return {sale_return.quantity} unit(s) -- only "
                f"{remaining} of {sale_item.quantity} remain returnable "
                f"for this sale item."
            )

        db_return = self.sale_return_repository.create(
            db,
            sale_return.sale_item_id,
            sale_return.quantity,
            sale_return.reason,
        )

        self.inventory_service.create_transaction(
            db,
            InventoryTransactionCreate(
                product_id=sale_item.product_id,
                transaction_type=TransactionType.RETURN,
                quantity_change=sale_return.quantity,
            ),
        )

        return db_return

    def get_all(
        self,
        db: Session,
        page: int,
        page_size: int,
    ):

        returns = self.sale_return_repository.get_all(
            db, page, page_size
        )

        total = self.sale_return_repository.count(db)

        return PaginatedResponse.create(
            items=returns,
            page=page,
            page_size=page_size,
            total=total,
        )
