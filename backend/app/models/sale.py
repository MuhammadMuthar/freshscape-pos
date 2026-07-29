from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Enum as SqlEnum,
    ForeignKey,
    Numeric,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums.payment_method import PaymentMethod
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.sale_item import SaleItem


class Sale(BaseModel):
    __tablename__ = "sales"

    customer_id: Mapped[int | None] = mapped_column(
        ForeignKey("customers.id"),
        nullable=True,
    )

    payment_method: Mapped[PaymentMethod] = mapped_column(
        SqlEnum(
            PaymentMethod,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
        ),
        nullable=False,
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="sales"
    )

    items: Mapped[list["SaleItem"]] = relationship(
        back_populates="sale",
        cascade="all, delete-orphan",
    )
