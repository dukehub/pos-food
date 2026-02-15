from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    phone: str | None = Field(default=None, max_length=32)
    email: str | None = Field(default=None, max_length=160)
    nif: str | None = Field(default=None, max_length=64)
    ai: str | None = Field(default=None, max_length=64)
    rc: str | None = Field(default=None, max_length=64)
    tax_id: str | None = Field(default=None, max_length=64)
    address: str | None = Field(default=None, max_length=255)
    credit_limit: Decimal | None = None
    payment_due_days: int = Field(default=30, ge=1, le=365)
    phone_whatsapp: str | None = Field(default=None, max_length=32)
    allow_notifications: bool = True
    is_active: bool = True


class CustomerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    phone: str | None
    email: str | None
    nif: str | None
    ai: str | None
    rc: str | None
    tax_id: str | None
    address: str | None
    current_balance: Decimal
    credit_limit: Decimal | None
    payment_due_days: int
    phone_whatsapp: str | None
    allow_notifications: bool
    is_active: bool
