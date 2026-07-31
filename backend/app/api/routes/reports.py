from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.schemas.report import DailySummaryResponse, LowStockProductResponse
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

service = ReportService()


@router.get(
    "/low-stock",
    response_model=list[LowStockProductResponse],
)
def get_low_stock(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_low_stock(db)


@router.get(
    "/daily-summary",
    response_model=DailySummaryResponse,
)
def get_daily_summary(
    target_date: date | None = Query(None, alias="date"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_daily_summary(db, target_date or date.today())
