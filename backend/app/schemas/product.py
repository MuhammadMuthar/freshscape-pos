from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.enums.product_unit import ProductUnit


class ProductBase(BaseModel):
    barcode: str
    sku: str
    name: str
    description: str | None = None

    cost_price: Decimal
    selling_price: Decimal

    stock_quantity: int
    minimum_stock: int

    unit: ProductUnit

    is_active: bool = True

    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    barcode: str | None = None
    sku: str | None = None
    name: str | None = None
    description: str | None = None

    cost_price: Decimal | None = None
    selling_price: Decimal | None = None

    stock_quantity: int | None = None
    minimum_stock: int | None = None

    unit: ProductUnit | None = None

    is_active: bool | None = None

    category_id: int | None = None


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )