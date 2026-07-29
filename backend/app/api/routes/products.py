from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.schemas.pagination import PaginatedResponse

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
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
    current_user=Depends(get_current_user),
):
    return service.create(db, product)


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
    current_user=Depends(get_current_user),
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


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_by_id(db, product_id)


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.update(db, product_id, product)


@router.delete(
    "/{product_id}",
    response_model=ProductResponse,
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.delete(db, product_id)
