from sqlalchemy import (
    Boolean,
    Enum as SqlEnum,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.enums.user_role import UserRole
from app.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        unique=True,
        nullable=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(
            UserRole,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
        ),
        default=UserRole.CASHIER,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )
