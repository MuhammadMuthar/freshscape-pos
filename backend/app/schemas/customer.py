from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    name: str
    phone: str | None = None
    email: str | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )
