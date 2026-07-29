from sqlalchemy.orm import Session

from app.repositories.supplier_repository import SupplierRepository
from app.schemas.supplier import SupplierCreate


class SupplierService:

    def __init__(self):
        self.supplier_repository = SupplierRepository()

    def create(
        self,
        db: Session,
        supplier: SupplierCreate,
    ):
        return self.supplier_repository.create(db, supplier)

    def get_all(
        self,
        db: Session,
    ):
        return self.supplier_repository.get_all(db)
