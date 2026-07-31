from datetime import date as date_type

from pydantic import BaseModel, ConfigDict

from app.enums.transaction_type import TransactionType
from app.schemas.category import CategorySimpleResponse


class LowStockProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    stock_quantity: int
    minimum_stock: int
    category: CategorySimpleResponse

    model_config = ConfigDict(
        from_attributes=True
    )


class DailySummaryBreakdown(BaseModel):
    transaction_type: TransactionType
    transaction_count: int
    net_quantity_change: int


class DailySummaryResponse(BaseModel):
    date: date_type
    total_transactions: int
    net_quantity_change: int
    breakdown: list[DailySummaryBreakdown]
