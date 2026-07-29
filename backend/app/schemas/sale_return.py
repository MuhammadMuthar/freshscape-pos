from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SaleReturnCreate(BaseModel):
    sale_item_id: int
    quantity: int = Field(gt=0)
    reason: str | None = None


class SaleReturnResponse(BaseModel):
    id: int
    sale_item_id: int
    quantity: int
    reason: str | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
