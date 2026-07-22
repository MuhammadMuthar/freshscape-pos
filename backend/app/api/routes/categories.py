from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
)
from app.services.category_service import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

service = CategoryService()


@router.post(
    "",
    response_model=CategoryResponse
)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    return service.create(
        db,
        category
    )


@router.get(
    "",
    response_model=list[CategoryResponse]
)
def get_categories(
    db: Session = Depends(get_db)
):
    return service.get_all(db)