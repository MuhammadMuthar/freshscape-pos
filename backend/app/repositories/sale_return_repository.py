from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from app.models.sale_return import SaleReturn


class SaleReturnRepository:

    def create(
        self,
        db: Session,
        sale_item_id: int,
        quantity: int,
        reason: str | None,
    ) -> SaleReturn:

        db_return = SaleReturn(
            sale_item_id=sale_item_id,
            quantity=quantity,
            reason=reason,
        )

        db.add(db_return)
        db.commit()
        db.refresh(db_return)

        return db_return

    def get_total_returned(
        self,
        db: Session,
        sale_item_id: int,
    ) -> int:

        statement = (
            select(func.coalesce(func.sum(SaleReturn.quantity), 0))
            .where(SaleReturn.sale_item_id == sale_item_id)
        )

        return db.execute(statement).scalar_one()

    def get_all(
        self,
        db: Session,
        page: int,
        page_size: int,
    ) -> list[SaleReturn]:

        offset = (page - 1) * page_size

        statement = (
            select(SaleReturn)
            .order_by(desc(SaleReturn.created_at))
            .offset(offset)
            .limit(page_size)
        )

        return list(db.execute(statement).scalars().all())

    def count(
        self,
        db: Session,
    ) -> int:

        statement = select(func.count(SaleReturn.id))

        return db.execute(statement).scalar_one()
