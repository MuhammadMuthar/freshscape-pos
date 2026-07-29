from sqlalchemy.orm import Session

from app.core.exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from app.repositories.category_repository import CategoryRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    def __init__(self):
        self.repository = CategoryRepository()
        self.product_repository = ProductRepository()

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

    def get_by_id(
        self,
        db: Session,
        category_id: int,
    ):
        category = self.repository.get_by_id(db, category_id)

        if category is None:
            raise NotFoundException("Category")

        return category

    def update(
        self,
        db: Session,
        category_id: int,
        category_update: CategoryUpdate,
    ):
        category = self.repository.get_by_id(db, category_id)

        if category is None:
            raise NotFoundException("Category")

        update_data = category_update.model_dump(exclude_unset=True)

        new_name = update_data.get("name")

        if new_name is not None and new_name != category.name:
            existing = self.repository.get_by_name(db, new_name)

            if existing is not None and existing.id != category.id:
                raise ConflictException(
                    "A category with this name already exists."
                )

        return self.repository.update(db, category, update_data)

    def delete(
        self,
        db: Session,
        category_id: int,
    ):
        category = self.repository.get_by_id(db, category_id)

        if category is None:
            raise NotFoundException("Category")

        product_count = self.product_repository.count(
            db,
            category_id=category_id,
        )

        if product_count > 0:
            raise BadRequestException(
                f"Cannot delete '{category.name}' -- {product_count} "
                f"product(s) are still assigned to it. Reassign or "
                f"remove them first."
            )

        self.repository.delete(db, category)
