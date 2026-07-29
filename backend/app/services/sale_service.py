from collections import defaultdict

from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException, NotFoundException
from app.enums.transaction_type import TransactionType
from app.repositories.customer_repository import CustomerRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.sale_repository import SaleRepository
from app.schemas.inventory_transaction import InventoryTransactionCreate
from app.schemas.pagination import PaginatedResponse
from app.schemas.sale import SaleCreate
from app.services.inventory_service import InventoryService


class SaleService:

    def __init__(self):
        self.sale_repository = SaleRepository()
        self.customer_repository = CustomerRepository()
        self.product_repository = ProductRepository()
        self.inventory_service = InventoryService()

    def create(
        self,
        db: Session,
        sale: SaleCreate,
    ):

        if sale.customer_id is not None:
            customer = self.customer_repository.get_by_id(
                db, sale.customer_id
            )

            if customer is None:
                raise NotFoundException("Customer")

        # Resolve products and default prices first, and validate total
        # demand per product against current stock BEFORE creating
        # anything. InventoryService commits each transaction as it goes,
        # so for a multi-item cart we can't rely on a single rollback if
        # a later line item turns out to be unfulfillable -- checking
        # everything up front keeps a rejected sale from partially
        # applying.
        products_by_id = {}
        resolved_items = []
        requested_quantity_by_product = defaultdict(int)

        for item in sale.items:
            product = products_by_id.get(item.product_id)

            if product is None:
                product = self.product_repository.get_by_id(
                    db, item.product_id
                )

                if product is None:
                    raise NotFoundException(f"Product {item.product_id}")

                products_by_id[item.product_id] = product

            unit_price = (
                item.unit_price
                if item.unit_price is not None
                else product.selling_price
            )

            resolved_items.append(
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "unit_price": unit_price,
                }
            )

            requested_quantity_by_product[item.product_id] += item.quantity

        for product_id, requested_quantity in requested_quantity_by_product.items():
            product = products_by_id[product_id]

            if product.stock_quantity < requested_quantity:
                raise BadRequestException(
                    f"Not enough stock for '{product.name}'. "
                    f"Available: {product.stock_quantity}, "
                    f"requested: {requested_quantity}."
                )

        total_amount = sum(
            item["quantity"] * item["unit_price"]
            for item in resolved_items
        )

        db_sale = self.sale_repository.create(
            db,
            sale.customer_id,
            sale.payment_method,
            resolved_items,
            total_amount,
        )

        for item in resolved_items:
            self.inventory_service.create_transaction(
                db,
                InventoryTransactionCreate(
                    product_id=item["product_id"],
                    transaction_type=TransactionType.SALE,
                    quantity_change=-item["quantity"],
                ),
            )

        return db_sale

    def get_all(
        self,
        db: Session,
        page: int,
        page_size: int,
        customer_id: int | None = None,
    ):

        sales = self.sale_repository.get_all(
            db, page, page_size, customer_id
        )

        total = self.sale_repository.count(db, customer_id)

        return PaginatedResponse.create(
            items=sales,
            page=page,
            page_size=page_size,
            total=total,
        )

    def get_by_id(
        self,
        db: Session,
        sale_id: int,
    ):

        sale = self.sale_repository.get_by_id(db, sale_id)

        if sale is None:
            raise NotFoundException("Sale")

        return sale
