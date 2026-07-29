from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.schemas.supplier import SupplierCreate, SupplierResponse
from app.services.supplier_service import SupplierService

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)

service = SupplierService()


@router.post(
    "",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.create(db, supplier)


@router.get(
    "",
    response_model=list[SupplierResponse],
)
def get_suppliers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_all(db)
