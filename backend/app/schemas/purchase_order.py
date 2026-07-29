from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.enums.purchase_order_status import PurchaseOrderStatus
from app.schemas.product import ProductSimpleResponse
from app.schemas.supplier import SupplierResponse


class PurchaseOrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    unit_cost: Decimal = Field(ge=0)


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    items: list[PurchaseOrderItemCreate] = Field(min_length=1)


class PurchaseOrderItemResponse(BaseModel):
    id: int
    product: ProductSimpleResponse
    quantity: int
    unit_cost: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


class PurchaseOrderResponse(BaseModel):
    id: int
    supplier: SupplierResponse
    status: PurchaseOrderStatus
    total_cost: Decimal
    items: list[PurchaseOrderItemResponse]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
