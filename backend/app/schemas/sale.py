from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.enums.payment_method import PaymentMethod
from app.schemas.customer import CustomerResponse
from app.schemas.product import ProductSimpleResponse


class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_price: Decimal | None = Field(default=None, ge=0)


class SaleCreate(BaseModel):
    customer_id: int | None = None
    payment_method: PaymentMethod
    items: list[SaleItemCreate] = Field(min_length=1)


class SaleItemResponse(BaseModel):
    id: int
    product: ProductSimpleResponse
    quantity: int
    unit_price: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


class SaleResponse(BaseModel):
    id: int
    customer: CustomerResponse | None
    payment_method: PaymentMethod
    total_amount: Decimal
    items: list[SaleItemResponse]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
