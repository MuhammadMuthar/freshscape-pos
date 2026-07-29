from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.enums.purchase_order_status import PurchaseOrderStatus
from app.schemas.pagination import PaginatedResponse
from app.schemas.purchase_order import (
    PurchaseOrderCreate,
    PurchaseOrderResponse,
)
from app.services.purchase_order_service import PurchaseOrderService

router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"],
)

service = PurchaseOrderService()


@router.post(
    "",
    response_model=PurchaseOrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_purchase_order(
    order: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.create(db, order)


@router.get(
    "",
    response_model=PaginatedResponse[PurchaseOrderResponse],
)
def get_purchase_orders(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status_filter: PurchaseOrderStatus | None = Query(None, alias="status"),
    supplier_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_all(
        db, page, page_size, status_filter, supplier_id
    )


@router.post(
    "/{purchase_order_id}/receive",
    response_model=PurchaseOrderResponse,
)
def receive_purchase_order(
    purchase_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.receive(db, purchase_order_id)


@router.post(
    "/{purchase_order_id}/cancel",
    response_model=PurchaseOrderResponse,
)
def cancel_purchase_order(
    purchase_order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.cancel(db, purchase_order_id)
