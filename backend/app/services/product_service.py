from sqlalchemy.orm import Session

from app.core.exceptions import (
    BadRequestException,
    ConflictException,
)
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate


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

    def get_all(
        self,
        db: Session,
    ):
        return self.product_repository.get_all(db)