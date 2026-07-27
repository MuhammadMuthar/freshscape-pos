from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session, selectinload

from app.enums.transaction_type import TransactionType
from app.models.inventory_transaction import InventoryTransaction


class InventoryRepository:

    def create(
        self,
        db: Session,
        product_id: int,
        transaction_type: TransactionType,
        quantity_change: int,
        quantity_before: int,
        quantity_after: int,
        reason: str | None,
    ) -> InventoryTransaction:

        db_transaction = InventoryTransaction(
            product_id=product_id,
            transaction_type=transaction_type,
            quantity_change=quantity_change,
            quantity_before=quantity_before,
            quantity_after=quantity_after,
            reason=reason,
        )

        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)

        return db_transaction

    def _apply_filters(
        self,
        statement,
        product_id: int | None = None,
        transaction_type: TransactionType | None = None,
    ):

        if product_id is not None:
            statement = statement.where(
                InventoryTransaction.product_id == product_id
            )

        if transaction_type is not None:
            statement = statement.where(
                InventoryTransaction.transaction_type == transaction_type
            )

        return statement

    def get_all(
        self,
        db: Session,
        page: int,
        page_size: int,
        product_id: int | None = None,
        transaction_type: TransactionType | None = None,
    ) -> list[InventoryTransaction]:

        statement = (
            select(InventoryTransaction)
            .options(selectinload(InventoryTransaction.product))
        )

        statement = self._apply_filters(
            statement,
            product_id,
            transaction_type,
        )

        offset = (page - 1) * page_size

        statement = (
            statement
            .order_by(desc(InventoryTransaction.created_at))
            .offset(offset)
            .limit(page_size)
        )

        result = db.execute(statement)

        return list(result.scalars().all())

    def count(
        self,
        db: Session,
        product_id: int | None = None,
        transaction_type: TransactionType | None = None,
    ) -> int:

        statement = select(func.count(InventoryTransaction.id))

        statement = self._apply_filters(
            statement,
            product_id,
            transaction_type,
        )

        return db.execute(statement).scalar_one()
