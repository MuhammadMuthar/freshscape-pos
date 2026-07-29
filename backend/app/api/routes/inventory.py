from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.enums.transaction_type import TransactionType
from app.schemas.inventory_transaction import (
    InventoryTransactionCreate,
    InventoryTransactionResponse,
)
from app.schemas.pagination import PaginatedResponse
from app.services.inventory_service import InventoryService

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)

service = InventoryService()


@router.post(
    "/transactions",
    response_model=InventoryTransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(
    transaction: InventoryTransactionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.create_transaction(db, transaction)


@router.get(
    "/transactions",
    response_model=PaginatedResponse[InventoryTransactionResponse],
)
def get_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    product_id: int | None = Query(None),
    transaction_type: TransactionType | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_all(
        db,
        page,
        page_size,
        product_id,
        transaction_type,
    )
