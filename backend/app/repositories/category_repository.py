from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


class ProductRepository:

    def create(
        self,
        db: Session,
        product: ProductCreate,
    ) -> Product:

        db_product = Product(
            **product.model_dump()
        )

        db.add(db_product)
        db.commit()
        db.refresh(db_product)

        return db_product

    def get_all(
        self,
        db: Session,
    ) -> list[Product]:

        statement = select(Product)

        result = db.execute(statement)

        return list(result.scalars().all())

    def get_by_barcode(
        self,
        db: Session,
        barcode: str,
    ):

        statement = (
            select(Product)
            .where(Product.barcode == barcode)
        )

        return db.execute(statement).scalar_one_or_none()

    def get_by_sku(
        self,
        db: Session,
        sku: str,
    ):

        statement = (
            select(Product)
            .where(Product.sku == sku)
        )

        return db.execute(statement).scalar_one_or_none()