from datetime import date

from sqlalchemy.orm import Session

from app.enums.transaction_type import TransactionType
from app.repositories.inventory_repository import InventoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.report import DailySummaryBreakdown, DailySummaryResponse


class ReportService:

    def __init__(self):
        self.product_repository = ProductRepository()
        self.inventory_repository = InventoryRepository()

    def get_low_stock(
        self,
        db: Session,
    ):
        return self.product_repository.get_low_stock(db)

    def get_daily_summary(
        self,
        db: Session,
        target_date: date,
    ) -> DailySummaryResponse:

        rows = self.inventory_repository.get_daily_summary(
            db, target_date
        )

        breakdown = [
            DailySummaryBreakdown(
                transaction_type=row.transaction_type,
                transaction_count=row.count,
                net_quantity_change=row.net_change,
            )
            for row in rows
        ]

        return DailySummaryResponse(
            date=target_date,
            total_transactions=sum(b.transaction_count for b in breakdown),
            net_quantity_change=sum(b.net_quantity_change for b in breakdown),
            breakdown=breakdown,
        )
