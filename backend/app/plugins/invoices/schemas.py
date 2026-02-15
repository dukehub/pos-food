from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class InvoiceCreate(BaseModel):
    number: str = Field(min_length=1, max_length=50)
    customer_id: str | None = None
    customer_name: str | None = Field(default=None, max_length=120)
    customer_tax_id: str | None = Field(default=None, max_length=64)
    customer_address: str | None = Field(default=None, max_length=255)
    total_amount: Decimal = Field(default=Decimal("0"), ge=Decimal("0"))


class InvoiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    number: str
    customer_id: str | None
    customer_name: str | None
    customer_tax_id: str | None
    customer_address: str | None
    total_amount: Decimal
