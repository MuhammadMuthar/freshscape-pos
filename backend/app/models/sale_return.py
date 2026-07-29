from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.sale_item import SaleItem


class SaleReturn(BaseModel):
    __tablename__ = "sale_returns"

    sale_item_id: Mapped[int] = mapped_column(
        ForeignKey("sale_items.id"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    sale_item: Mapped["SaleItem"] = relationship(
        back_populates="returns"
    )
