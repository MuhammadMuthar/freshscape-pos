from decimal import Decimal
from typing import TYPE_CHECKING
from app.enums.product_unit import ProductUnit
from sqlalchemy import (
    Boolean,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.inventory_transaction import InventoryTransaction


class Product(BaseModel):
    __tablename__ = "products"

    barcode: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    cost_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    selling_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    stock_quantity: Mapped[int] = mapped_column(
        default=0,
    )

    minimum_stock: Mapped[int] = mapped_column(
        default=10,
    )

    from sqlalchemy import Enum as SqlEnum  

    unit: Mapped[ProductUnit] = mapped_column(
        SqlEnum(ProductUnit),
        default=ProductUnit.PCS,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
    )

    category: Mapped["Category"] = relationship(
        back_populates="products"
    )

    inventory_transactions: Mapped[list["InventoryTransaction"]] = relationship(
        back_populates="product"
    )