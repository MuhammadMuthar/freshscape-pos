from decimal import Decimal

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session, selectinload

from app.enums.payment_method import PaymentMethod
from app.models.sale import Sale
from app.models.sale_item import SaleItem


class SaleRepository:

    def create(
        self,
        db: Session,
        customer_id: int | None,
        payment_method: PaymentMethod,
        items: list[dict],
        total_amount: Decimal,
    ) -> Sale:

        db_sale = Sale(
            customer_id=customer_id,
            payment_method=payment_method,
            total_amount=total_amount,
        )

        db_sale.items = [
            SaleItem(**item) for item in items
        ]

        db.add(db_sale)
        db.commit()
        db.refresh(db_sale)

        return db_sale

    def _with_relations(self, statement):
        return statement.options(
            selectinload(Sale.customer),
            selectinload(Sale.items).selectinload(SaleItem.product),
        )

    def get_by_id(
        self,
        db: Session,
        sale_id: int,
    ):

        statement = self._with_relations(
            select(Sale).where(Sale.id == sale_id)
        )

        return db.execute(statement).scalar_one_or_none()

    def get_all(
        self,
        db: Session,
        page: int,
        page_size: int,
        customer_id: int | None = None,
    ) -> list[Sale]:

        statement = self._with_relations(select(Sale))

        if customer_id is not None:
            statement = statement.where(
                Sale.customer_id == customer_id
            )

        offset = (page - 1) * page_size

        statement = (
            statement
            .order_by(desc(Sale.created_at))
            .offset(offset)
            .limit(page_size)
        )

        return list(db.execute(statement).scalars().all())

    def count(
        self,
        db: Session,
        customer_id: int | None = None,
    ) -> int:

        statement = select(func.count(Sale.id))

        if customer_id is not None:
            statement = statement.where(
                Sale.customer_id == customer_id
            )

        return db.execute(statement).scalar_one()
