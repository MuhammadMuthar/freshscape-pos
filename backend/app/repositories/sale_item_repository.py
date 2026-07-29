from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.sale_item import SaleItem


class SaleItemRepository:

    def get_by_id(
        self,
        db: Session,
        sale_item_id: int,
    ):

        statement = (
            select(SaleItem)
            .options(selectinload(SaleItem.product))
            .where(SaleItem.id == sale_item_id)
        )

        return db.execute(statement).scalar_one_or_none()
