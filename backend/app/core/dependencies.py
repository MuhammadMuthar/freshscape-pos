from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenException, UnauthorizedException
from app.core.security import decode_access_token
from app.database.session import get_db
from app.enums.user_role import UserRole
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

user_repository = UserRepository()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")

        if username is None:
            raise UnauthorizedException()

    except JWTError:
        raise UnauthorizedException(
            "Invalid or expired authentication token."
        )

    user = user_repository.get_by_username(db, username)

    if user is None or not user.is_active:
        raise UnauthorizedException()

    return user


def require_role(*allowed_roles: UserRole):

    def dependency(current_user=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise ForbiddenException()

        return current_user

    return dependency
