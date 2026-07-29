from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Enum as SqlEnum,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.purchase_order_status import PurchaseOrderStatus
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.purchase_order_item import PurchaseOrderItem
    from app.models.supplier import Supplier


class PurchaseOrder(BaseModel):
    __tablename__ = "purchase_orders"

    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id"),
        nullable=False,
    )

    status: Mapped[PurchaseOrderStatus] = mapped_column(
        SqlEnum(
            PurchaseOrderStatus,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
        ),
        default=PurchaseOrderStatus.PENDING,
        nullable=False,
    )

    total_cost: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    supplier: Mapped["Supplier"] = relationship(
        back_populates="purchase_orders"
    )

    items: Mapped[list["PurchaseOrderItem"]] = relationship(
        back_populates="purchase_order",
        cascade="all, delete-orphan",
    )
