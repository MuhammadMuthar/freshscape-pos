from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


class CustomerRepository:

    def create(
        self,
        db: Session,
        customer: CustomerCreate,
    ) -> Customer:

        db_customer = Customer(
            **customer.model_dump()
        )

        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)

        return db_customer

    def get_all(
        self,
        db: Session,
    ) -> list[Customer]:

        statement = select(Customer)

        return list(db.execute(statement).scalars().all())

    def get_by_id(
        self,
        db: Session,
        customer_id: int,
    ):

        statement = (
            select(Customer)
            .where(Customer.id == customer_id)
        )

        return db.execute(statement).scalar_one_or_none()
