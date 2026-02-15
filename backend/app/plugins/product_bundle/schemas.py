from pydantic import BaseModel, ConfigDict, Field


class ProductBundleItemCreate(BaseModel):
    parent_product_id: str
    child_product_id: str
    quantity: int = Field(default=1, ge=1, le=50)
    is_active: bool = True


class ProductBundleItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    parent_product_id: str
    child_product_id: str
    quantity: int
    is_active: bool
