from sqlalchemy.orm import Session

from sqlalchemy import select

from app.models.category import Category
from app.schemas.category import CategoryCreate


class CategoryRepository:

    def create(
        self,
        db: Session,
        category: CategoryCreate
    ) -> Category:

        db_category = Category(
            name=category.name,
            description=category.description
        )

        db.add(db_category)
        db.commit()
        db.refresh(db_category)

        return db_category

    def get_all(
        self,
        db: Session
    ):

        return db.query(Category).all()

    def get_by_id(
        self,
        db: Session,
        category_id: int,
    ):
        statement = (
            select(Category)
            .where(Category.id == category_id)
        )

        return db.execute(statement).scalar_one_or_none()