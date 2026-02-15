from pydantic import BaseModel, ConfigDict, Field


class RestaurantConfigUpsert(BaseModel):
    name: str = Field(default="", max_length=120)
    slug: str = Field(default="", max_length=120)
    currency: str = Field(default="USD", max_length=16)
    locale: str = Field(default="fr", max_length=16)

    address: str = Field(default="", max_length=255)
    phone: str = Field(default="", max_length=32)
    email: str = Field(default="", max_length=160)

    tax_nif: str = Field(default="", max_length=64)
    tax_rc: str = Field(default="", max_length=64)
    tax_ai: str = Field(default="", max_length=64)

    logo_url: str = Field(default="", max_length=255)
    background_image_url: str = Field(default="", max_length=255)
    background_image_secondary_url: str = Field(default="", max_length=255)

    location_label: str = Field(default="", max_length=255)
    city: str = Field(default="", max_length=120)
    country: str = Field(default="", max_length=120)
    postal_code: str = Field(default="", max_length=32)
    latitude: str = Field(default="", max_length=32)
    longitude: str = Field(default="", max_length=32)


class RestaurantConfigOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str

    name: str
    slug: str
    currency: str
    locale: str

    address: str
    phone: str
    email: str

    tax_nif: str
    tax_rc: str
    tax_ai: str

    logo_url: str
    background_image_url: str
    background_image_secondary_url: str

    location_label: str
    city: str
    country: str
    postal_code: str
    latitude: str
    longitude: str
    is_active: bool

