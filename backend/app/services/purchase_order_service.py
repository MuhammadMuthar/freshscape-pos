from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException, NotFoundException
from app.enums.purchase_order_status import PurchaseOrderStatus
from app.enums.transaction_type import TransactionType
from app.repositories.product_repository import ProductRepository
from app.repositories.purchase_order_repository import PurchaseOrderRepository
from app.repositories.supplier_repository import SupplierRepository
from app.schemas.inventory_transaction import InventoryTransactionCreate
from app.schemas.pagination import PaginatedResponse
from app.schemas.purchase_order import PurchaseOrderCreate
from app.services.inventory_service import InventoryService


class PurchaseOrderService:

    def __init__(self):
        self.purchase_order_repository = PurchaseOrderRepository()
        self.supplier_repository = SupplierRepository()
        self.product_repository = ProductRepository()
        self.inventory_service = InventoryService()

    def create(
        self,
        db: Session,
        order: PurchaseOrderCreate,
    ):

        supplier = self.supplier_repository.get_by_id(
            db, order.supplier_id
        )

        if supplier is None:
            raise NotFoundException("Supplier")

        total_cost = 0

        for item in order.items:
            product = self.product_repository.get_by_id(
                db, item.product_id
            )

            if product is None:
                raise NotFoundException(f"Product {item.product_id}")

            total_cost += item.quantity * item.unit_cost

        items = [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "unit_cost": item.unit_cost,
            }
            for item in order.items
        ]

        return self.purchase_order_repository.create(
            db,
            order.supplier_id,
            items,
            total_cost,
        )

    def receive(
        self,
        db: Session,
        purchase_order_id: int,
    ):

        purchase_order = self.purchase_order_repository.get_by_id(
            db, purchase_order_id
        )

        if purchase_order is None:
            raise NotFoundException("Purchase order")

        if purchase_order.status != PurchaseOrderStatus.PENDING:
            raise BadRequestException(
                "Only pending purchase orders can be received."
            )

        for item in purchase_order.items:
            self.inventory_service.create_transaction(
                db,
                InventoryTransactionCreate(
                    product_id=item.product_id,
                    transaction_type=TransactionType.PURCHASE,
                    quantity_change=item.quantity,
                ),
            )

        return self.purchase_order_repository.update_status(
            db,
            purchase_order,
            PurchaseOrderStatus.RECEIVED,
        )

    def cancel(
        self,
        db: Session,
        purchase_order_id: int,
    ):

        purchase_order = self.purchase_order_repository.get_by_id(
            db, purchase_order_id
        )

        if purchase_order is None:
            raise NotFoundException("Purchase order")

        if purchase_order.status != PurchaseOrderStatus.PENDING:
            raise BadRequestException(
                "Only pending purchase orders can be cancelled."
            )

        return self.purchase_order_repository.update_status(
            db,
            purchase_order,
            PurchaseOrderStatus.CANCELLED,
        )

    def get_all(
        self,
        db: Session,
        page: int,
        page_size: int,
        status: PurchaseOrderStatus | None = None,
        supplier_id: int | None = None,
    ):

        orders = self.purchase_order_repository.get_all(
            db, page, page_size, status, supplier_id
        )

        total = self.purchase_order_repository.count(
            db, status, supplier_id
        )

        return PaginatedResponse.create(
            items=orders,
            page=page,
            page_size=page_size,
            total=total,
        )
