from sqlalchemy.orm import Session

from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate


class CustomerService:

    def __init__(self):
        self.customer_repository = CustomerRepository()

    def create(
        self,
        db: Session,
        customer: CustomerCreate,
    ):
        return self.customer_repository.create(db, customer)

    def get_all(
        self,
        db: Session,
    ):
        return self.customer_repository.get_all(db)
