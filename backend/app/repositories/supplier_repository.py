from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate


class SupplierRepository:

    def create(
        self,
        db: Session,
        supplier: SupplierCreate,
    ) -> Supplier:

        db_supplier = Supplier(
            **supplier.model_dump()
        )

        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)

        return db_supplier

    def get_all(
        self,
        db: Session,
    ) -> list[Supplier]:

        statement = select(Supplier)

        return list(db.execute(statement).scalars().all())

    def get_by_id(
        self,
        db: Session,
        supplier_id: int,
    ):

        statement = (
            select(Supplier)
            .where(Supplier.id == supplier_id)
        )

        return db.execute(statement).scalar_one_or_none()
