from sqlalchemy.orm import Session

from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate


class CategoryService:

    def __init__(self):
        self.repository = CategoryRepository()

    def create(
        self,
        db: Session,
        category: CategoryCreate
    ):
        return self.repository.create(
            db,
            category
        )

    def get_all(
        self,
        db: Session
    ):
        return self.repository.get_all(db)