from sqlalchemy.orm import Session

from app.core.exceptions import ConflictException, UnauthorizedException
from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.user import Token, UserCreate


class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()

    def register(
        self,
        db: Session,
        user: UserCreate,
    ):
        if self.user_repository.get_by_username(db, user.username):
            raise ConflictException(
                "Username already exists."
            )

        return self.user_repository.create(db, user)

    def login(
        self,
        db: Session,
        username: str,
        password: str,
    ) -> Token:

        user = self.user_repository.get_by_username(db, username)

        if user is None or not verify_password(
            password, user.hashed_password
        ):
            raise UnauthorizedException(
                "Incorrect username or password."
            )

        if not user.is_active:
            raise UnauthorizedException(
                "This account has been deactivated."
            )

        access_token = create_access_token(
            {"sub": user.username, "role": user.role.value}
        )

        return Token(access_token=access_token)
