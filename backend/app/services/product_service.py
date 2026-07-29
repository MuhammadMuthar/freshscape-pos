from sqlalchemy.orm import Session
from app.schemas.pagination import PaginatedResponse

from app.core.exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    def __init__(self):
        self.product_repository = ProductRepository()
        self.category_repository = CategoryRepository()

    def create(
        self,
        db: Session,
        product: ProductCreate,
    ):
        if self.product_repository.get_by_barcode(
            db,
            product.barcode,
        ):
            raise ConflictException(
                "Barcode already exists."
            )
        
        if self.product_repository.get_by_sku(
            db,
            product.sku,
        ):
            raise ConflictException(
                "SKU already exists."
            )

        if product.cost_price < 0:
            raise BadRequestException(
                "Cost price cannot be negative"
            )
        
        if product.selling_price < product.cost_price:
            raise BadRequestException(
                "Selling price cannot be lower than cost price."
            )

        if product.stock_quantity < 0:
            raise BadRequestException(
                "Stock quantity cannot be negative."
            )

        if product.minimum_stock < 0:
            raise BadRequestException(
                "Minimum stock cannot be negative."
            )

        category = self.category_repository.get_by_id(
            db,
            product.category_id,
        )

        if category is None:
            raise BadRequestException(
                "Category does not exist."
            )
        return self.product_repository.create(
            db,
            product,
        )

    def get_by_id(
        self,
        db: Session,
        product_id: int,
    ):
        product = self.product_repository.get_by_id_detailed(
            db,
            product_id,
        )

        if product is None:
            raise NotFoundException("Product")

        return product

    def update(
        self,
        db: Session,
        product_id: int,
        product_update: ProductUpdate,
    ):
        product = self.product_repository.get_by_id(
            db,
            product_id,
        )

        if product is None:
            raise NotFoundException("Product")

        update_data = product_update.model_dump(exclude_unset=True)

        # Stock must only ever change through an inventory transaction so
        # the ledger stays accurate -- editing it here would silently
        # desync stock_quantity from the audit trail.
        if "stock_quantity" in update_data:
            raise BadRequestException(
                "Stock quantity can't be edited directly here. "
                "Use POST /inventory/transactions (transaction_type: "
                "'adjustment') so the change is recorded in the ledger."
            )

        new_barcode = update_data.get("barcode")

        if new_barcode is not None and new_barcode != product.barcode:
            existing = self.product_repository.get_by_barcode(
                db,
                new_barcode,
            )

            if existing is not None and existing.id != product.id:
                raise ConflictException(
                    "Barcode already exists."
                )

        new_sku = update_data.get("sku")

        if new_sku is not None and new_sku != product.sku:
            existing = self.product_repository.get_by_sku(
                db,
                new_sku,
            )

            if existing is not None and existing.id != product.id:
                raise ConflictException(
                    "SKU already exists."
                )

        new_category_id = update_data.get("category_id")

        if new_category_id is not None:
            category = self.category_repository.get_by_id(
                db,
                new_category_id,
            )

            if category is None:
                raise BadRequestException(
                    "Category does not exist."
                )

        cost_price = update_data.get("cost_price", product.cost_price)
        selling_price = update_data.get(
            "selling_price", product.selling_price
        )

        if cost_price < 0:
            raise BadRequestException(
                "Cost price cannot be negative."
            )

        if selling_price < cost_price:
            raise BadRequestException(
                "Selling price cannot be lower than cost price."
            )

        minimum_stock = update_data.get(
            "minimum_stock", product.minimum_stock
        )

        if minimum_stock < 0:
            raise BadRequestException(
                "Minimum stock cannot be negative."
            )

        return self.product_repository.update(
            db,
            product,
            update_data,
        )

    def delete(
        self,
        db: Session,
        product_id: int,
    ):
        product = self.product_repository.get_by_id(
            db,
            product_id,
        )

        if product is None:
            raise NotFoundException("Product")

        return self.product_repository.deactivate(
            db,
            product,
        )

    def get_all(
        self,
        db: Session,
        page: int,
        page_size: int,
        search: str | None = None,
        category_id: int | None = None,
        is_active: bool | None = None,
        sort_by: str = "name",
        order: str = "asc",
    ):
        products = self.product_repository.get_all(
            db,
            page,
            page_size,
            search,
            category_id,
            is_active,
            sort_by,
            order,
        )

        total = self.product_repository.count(
            db,
            search,
            category_id,
            is_active,
        )

        return PaginatedResponse.create(
            items=products,
            page=page,
            page_size=page_size,
            total=total,
        )