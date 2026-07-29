from decimal import Decimal

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session, selectinload

from app.enums.purchase_order_status import PurchaseOrderStatus
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_item import PurchaseOrderItem


class PurchaseOrderRepository:

    def create(
        self,
        db: Session,
        supplier_id: int,
        items: list[dict],
        total_cost: Decimal,
    ) -> PurchaseOrder:

        db_order = PurchaseOrder(
            supplier_id=supplier_id,
            status=PurchaseOrderStatus.PENDING,
            total_cost=total_cost,
        )

        db_order.items = [
            PurchaseOrderItem(**item) for item in items
        ]

        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        return db_order

    def _with_relations(self, statement):
        return statement.options(
            selectinload(PurchaseOrder.supplier),
            selectinload(PurchaseOrder.items).selectinload(
                PurchaseOrderItem.product
            ),
        )

    def get_by_id(
        self,
        db: Session,
        purchase_order_id: int,
    ):

        statement = self._with_relations(
            select(PurchaseOrder)
            .where(PurchaseOrder.id == purchase_order_id)
        )

        return db.execute(statement).scalar_one_or_none()

    def get_all(
        self,
        db: Session,
        page: int,
        page_size: int,
        status: PurchaseOrderStatus | None = None,
        supplier_id: int | None = None,
    ) -> list[PurchaseOrder]:

        statement = self._with_relations(select(PurchaseOrder))

        if status is not None:
            statement = statement.where(
                PurchaseOrder.status == status
            )

        if supplier_id is not None:
            statement = statement.where(
                PurchaseOrder.supplier_id == supplier_id
            )

        offset = (page - 1) * page_size

        statement = (
            statement
            .order_by(desc(PurchaseOrder.created_at))
            .offset(offset)
            .limit(page_size)
        )

        return list(db.execute(statement).scalars().all())

    def count(
        self,
        db: Session,
        status: PurchaseOrderStatus | None = None,
        supplier_id: int | None = None,
    ) -> int:

        statement = select(func.count(PurchaseOrder.id))

        if status is not None:
            statement = statement.where(
                PurchaseOrder.status == status
            )

        if supplier_id is not None:
            statement = statement.where(
                PurchaseOrder.supplier_id == supplier_id
            )

        return db.execute(statement).scalar_one()

    def update_status(
        self,
        db: Session,
        purchase_order: PurchaseOrder,
        status: PurchaseOrderStatus,
    ) -> PurchaseOrder:

        purchase_order.status = status

        db.add(purchase_order)
        db.commit()
        db.refresh(purchase_order)

        return purchase_order
