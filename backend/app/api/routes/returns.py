from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.schemas.pagination import PaginatedResponse
from app.schemas.sale_return import SaleReturnCreate, SaleReturnResponse
from app.services.sale_return_service import SaleReturnService

router = APIRouter(
    prefix="/returns",
    tags=["Returns"],
)

service = SaleReturnService()


@router.post(
    "",
    response_model=SaleReturnResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_return(
    sale_return: SaleReturnCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.create(db, sale_return)


@router.get(
    "",
    response_model=PaginatedResponse[SaleReturnResponse],
)
def get_returns(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_all(db, page, page_size)
