from typing import TYPE_CHECKING

from sqlalchemy import (
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.enums.transaction_type import TransactionType
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.product import Product


class InventoryTransaction(BaseModel):
    __tablename__ = "inventory_transactions"

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    transaction_type: Mapped[TransactionType] = mapped_column(
        SqlEnum(
            TransactionType,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
        ),
        nullable=False,
    )

    quantity_change: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    quantity_before: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    quantity_after: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    product: Mapped["Product"] = relationship(
        back_populates="inventory_transactions"
    )
