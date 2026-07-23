from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.pagination import PaginatedResponse

from app.database.session import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

service = ProductService()


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    return service.create(db, product)

from fastapi import Query


@router.get(
    "",
    response_model=PaginatedResponse[ProductResponse],
)

def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    category_id: int | None = Query(None),
    is_active: bool | None = Query(None),
    sort_by: str = Query("name"),
    order: str = Query("asc"),
    db: Session = Depends(get_db),
):
    return service.get_all(
        db,
        page,
        page_size,
        search,
        category_id,
        is_active,
        sort_by,
        order,
    )