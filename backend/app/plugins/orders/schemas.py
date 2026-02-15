from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class OrderLineCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    quantity: int = Field(ge=1, default=1)
    unit_price: Decimal = Field(ge=0, default=Decimal("0.00"))
    product_id: str | None = None
    variant_id: str | None = None


class OrderCreate(BaseModel):
    status: str = Field(default="draft", min_length=1, max_length=30)
    note: str | None = Field(default=None, max_length=255)
    lines: list[OrderLineCreate] = Field(default_factory=list)


class OrderLineOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    product_id: str | None
    variant_id: str | None
    name: str
    quantity: int
    unit_price: Decimal
    line_total: Decimal


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    status: str
    note: str | None
    total_amount: Decimal
    lines: list[OrderLineOut] = Field(default_factory=list)

