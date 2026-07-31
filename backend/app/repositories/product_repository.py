from sqlalchemy import select
from sqlalchemy.orm import Session

from sqlalchemy import asc, desc

from sqlalchemy import or_, func

from sqlalchemy import func
from app.schemas.pagination import PaginatedResponse

from sqlalchemy.orm import selectinload

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

    from sqlalchemy import select
    from sqlalchemy.orm import Session, selectinload

    from app.models.product import Product

    def _apply_filters(
        self,
        statement,
        search: str | None = None,
        category_id: int | None = None,
        is_active: bool | None = None,
    ):

        if search:
            statement = statement.where(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.barcode.ilike(f"%{search}%"),
                    Product.sku.ilike(f"%{search}%"),
                )
            )

        if category_id is not None:
            statement = statement.where(
                Product.category_id == category_id
            )

        if is_active is not None:
            statement = statement.where(
                Product.is_active == is_active
            )

        return statement


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
    ) -> list[Product]:

        statement = (
            select(Product)
            .options(selectinload(Product.category))
        )

        statement = self._apply_filters(
            statement,
            search,
            category_id,
            is_active,
        )

        offset = (page - 1) * page_size

        sortable_columns = {
            "name": Product.name,
            "selling_price": Product.selling_price,
            "stock_quantity": Product.stock_quantity,
            "created_at": Product.created_at,
        }

        column = sortable_columns.get(sort_by, Product.name)

        if order.lower() == "desc":
            statement = statement.order_by(desc(column))
        else:
            statement = statement.order_by(asc(column))

        statement = (
            statement
            .offset(offset)
            .limit(page_size)
        )

        result = db.execute(statement)

        return list(result.scalars().all())

    def get_low_stock(
        self,
        db: Session,
    ):
        statement = (
            select(Product)
            .options(selectinload(Product.category))
            .where(
                Product.is_active == True,  # noqa: E712
                Product.stock_quantity <= Product.minimum_stock,
            )
            .order_by(Product.stock_quantity)
        )

        return list(db.execute(statement).scalars().all())

    def get_by_id(
        self,
        db: Session,
        product_id: int,
    ):

        statement = (
            select(Product)
            .where(Product.id == product_id)
        )

        return db.execute(statement).scalar_one_or_none()

    def get_by_id_detailed(
        self,
        db: Session,
        product_id: int,
    ):

        statement = (
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.id == product_id)
        )

        return db.execute(statement).scalar_one_or_none()

    def update(
        self,
        db: Session,
        product: Product,
        update_data: dict,
    ) -> Product:

        for field, value in update_data.items():
            setattr(product, field, value)

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    def deactivate(
        self,
        db: Session,
        product: Product,
    ) -> Product:

        product.is_active = False

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    def update_stock(
        self,
        db: Session,
        product: Product,
        new_stock_quantity: int,
    ) -> Product:

        product.stock_quantity = new_stock_quantity

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

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

    def count(
        self,
        db: Session,
        search: str | None = None,
        category_id: int | None = None,
        is_active: bool | None = None,
    ) -> int:

        statement = select(func.count(Product.id))

        statement = self._apply_filters(
            statement,
            search,
            category_id,
            is_active,
        )

        return db.execute(statement).scalar_one()