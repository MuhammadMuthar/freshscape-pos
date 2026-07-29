from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.product import Product
    from app.models.sale import Sale
    from app.models.sale_return import SaleReturn


class SaleItem(BaseModel):
    __tablename__ = "sale_items"

    sale_id: Mapped[int] = mapped_column(
        ForeignKey("sales.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    sale: Mapped["Sale"] = relationship(
        back_populates="items"
    )

    product: Mapped["Product"] = relationship(
        back_populates="sale_items"
    )

    returns: Mapped[list["SaleReturn"]] = relationship(
        back_populates="sale_item"
    )
