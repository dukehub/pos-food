import enum

from pydantic import BaseModel, ConfigDict, Field


class TemplateType(str, enum.Enum):
    CUSTOMER_RECEIPT = "ticket_client"
    KITCHEN_TICKET = "ticket_cuisine"
    INVOICE = "facture_a4"


class TicketTemplateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    template_type: TemplateType = TemplateType.KITCHEN_TICKET
    structure_json: dict = Field(default_factory=dict)
    is_active: bool = True


class TicketTemplateOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    template_type: TemplateType
    structure_json: dict
    is_active: bool
