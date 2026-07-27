from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.transaction_type import TransactionType
from app.schemas.product import ProductSimpleResponse


class InventoryTransactionCreate(BaseModel):
    product_id: int
    transaction_type: TransactionType

    quantity_change: int

    reason: str | None = None


class InventoryTransactionResponse(BaseModel):
    id: int

    product_id: int
    transaction_type: TransactionType

    quantity_change: int
    quantity_before: int
    quantity_after: int

    reason: str | None = None

    created_at: datetime

    product: ProductSimpleResponse

    model_config = ConfigDict(
        from_attributes=True
    )
