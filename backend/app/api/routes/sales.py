from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.schemas.pagination import PaginatedResponse
from app.schemas.sale import SaleCreate, SaleResponse
from app.services.sale_service import SaleService

router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)

service = SaleService()


@router.post(
    "",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.create(db, sale)


@router.get(
    "",
    response_model=PaginatedResponse[SaleResponse],
)
def get_sales(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    customer_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_all(db, page, page_size, customer_id)


@router.get(
    "/{sale_id}",
    response_model=SaleResponse,
)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_by_id(db, sale_id)
