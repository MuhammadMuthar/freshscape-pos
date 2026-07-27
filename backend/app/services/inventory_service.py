from sqlalchemy.orm import Session

from app.core.exceptions import (
    BadRequestException,
    NotFoundException,
)
from app.enums.transaction_type import TransactionType
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.inventory_transaction import InventoryTransactionCreate
from app.schemas.pagination import PaginatedResponse


class InventoryService:

    def __init__(self):
        self.inventory_repository = InventoryRepository()
        self.product_repository = ProductRepository()

    def _validate_direction(
        self,
        transaction_type: TransactionType,
        quantity_change: int,
    ):

        if quantity_change == 0:
            raise BadRequestException(
                "Quantity change cannot be zero."
            )

        if transaction_type == TransactionType.PURCHASE and quantity_change < 0:
            raise BadRequestException(
                "Purchase transactions must increase stock."
            )

        if transaction_type == TransactionType.RETURN and quantity_change < 0:
            raise BadRequestException(
                "Return transactions must increase stock."
            )

        if transaction_type == TransactionType.SALE and quantity_change > 0:
            raise BadRequestException(
                "Sale transactions must decrease stock."
            )

    def create_transaction(
        self,
        db: Session,
        transaction: InventoryTransactionCreate,
    ):

        product = self.product_repository.get_by_id(
            db,
            transaction.product_id,
        )

        if product is None:
            raise NotFoundException("Product")

        self._validate_direction(
            transaction.transaction_type,
            transaction.quantity_change,
        )

        if transaction.transaction_type == TransactionType.ADJUSTMENT:
            if not transaction.reason or not transaction.reason.strip():
                raise BadRequestException(
                    "Manual adjustments require a reason."
                )

        quantity_before = product.stock_quantity
        quantity_after = quantity_before + transaction.quantity_change

        if quantity_after < 0:
            raise BadRequestException(
                "Transaction would result in negative stock."
            )

        self.product_repository.update_stock(
            db,
            product,
            quantity_after,
        )

        return self.inventory_repository.create(
            db,
            product_id=transaction.product_id,
            transaction_type=transaction.transaction_type,
            quantity_change=transaction.quantity_change,
            quantity_before=quantity_before,
            quantity_after=quantity_after,
            reason=transaction.reason,
        )

    def get_all(
        self,
        db: Session,
        page: int,
        page_size: int,
        product_id: int | None = None,
        transaction_type: TransactionType | None = None,
    ):

        transactions = self.inventory_repository.get_all(
            db,
            page,
            page_size,
            product_id,
            transaction_type,
        )

        total = self.inventory_repository.count(
            db,
            product_id,
            transaction_type,
        )

        return PaginatedResponse.create(
            items=transactions,
            page=page,
            page_size=page_size,
            total=total,
        )
