from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:

    def create(
        self,
        db: Session,
        user: UserCreate,
    ) -> User:

        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            role=user.role,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    def get_by_username(
        self,
        db: Session,
        username: str,
    ):

        statement = (
            select(User)
            .where(User.username == username)
        )

        return db.execute(statement).scalar_one_or_none()

    def get_by_id(
        self,
        db: Session,
        user_id: int,
    ):

        statement = (
            select(User)
            .where(User.id == user_id)
        )

        return db.execute(statement).scalar_one_or_none()
