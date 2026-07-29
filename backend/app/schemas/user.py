from pydantic import BaseModel, ConfigDict, Field

from app.enums.user_role import UserRole


class UserCreate(BaseModel):
    username: str
    email: str | None = None
    password: str = Field(min_length=8)
    role: UserRole = UserRole.CASHIER


class UserResponse(BaseModel):
    id: int
    username: str
    email: str | None
    role: UserRole
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
