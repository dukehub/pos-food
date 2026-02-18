import enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

# --- Enums ---
class SelectionMode(str, enum.Enum):
    SINGLE = "single"
    MULTI = "multi"

# --- Modifiers ---

class ModifierItemBase(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=100)
    price_delta: float = 0.0
    is_active: bool = True
    sort_order: int = 0

class ModifierItemCreate(ModifierItemBase):
    pass

class ModifierItemUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price_delta: Optional[float] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None

class ModifierItemOut(ModifierItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    group_id: str

class ModifierGroupBase(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=100)
    selection_mode: SelectionMode = SelectionMode.SINGLE
    min_select: int = 0
    max_select: int = 1
    is_active: bool = True
    sort_order: int = 0

class ModifierGroupCreate(ModifierGroupBase):
    items: List[ModifierItemCreate] = []

class ModifierGroupUpdate(BaseModel):
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    selection_mode: Optional[SelectionMode] = None
    min_select: Optional[int] = None
    max_select: Optional[int] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None
    # We won't handle items update here nestedly for simplicity, separate endpoints for items recommended
    # or full replacement strategy.

class ModifierGroupOut(ModifierGroupBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    items: List[ModifierItemOut] = []

# --- Custom Type for Linking Modifiers ---
class ModifierGroupLink(BaseModel):
    group_id: str

# --- Variants ---

class ProductVariantBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    variant_key: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    default_price: float = 0.0
    sku: Optional[str] = Field(None, max_length=50)
    is_active: bool = True
    sort_order: int = 0
    image_url: Optional[str] = Field(None, max_length=255)

class ProductVariantCreate(ProductVariantBase):
    modifier_group_ids: List[str] = []

class ProductVariantUpdate(BaseModel):
    name: Optional[str] = None
    variant_key: Optional[str] = None
    description: Optional[str] = None
    default_price: Optional[float] = None
    sku: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None
    image_url: Optional[str] = None
    modifier_group_ids: Optional[List[str]] = None

class ProductVariantOut(ProductVariantBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    product_id: str
    modifier_groups: List[ModifierGroupOut] = []

# --- Products ---

class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    slug: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    sku: Optional[str] = Field(None, max_length=50)
    is_active: bool = True
    sort_order: int = 0
    image_url: Optional[str] = Field(None, max_length=255)
    category_id: Optional[str] = None

class ProductCreate(ProductBase):
    modifier_group_ids: List[str] = []
    # Variants usually created separately or nested? Let's allow nested creation for initial setup
    variants: List[ProductVariantCreate] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    sku: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None
    image_url: Optional[str] = None
    category_id: Optional[str] = None
    modifier_group_ids: Optional[List[str]] = None

class ProductOut(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    variants: List[ProductVariantOut] = []
    modifier_groups: List[ModifierGroupOut] = []

# --- Categories ---

class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    slug: str = Field(min_length=1, max_length=50)
    is_active: bool = True
    sort_order: int = 0
    parent_id: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None
    parent_id: Optional[str] = None

class CategoryOut(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: str
    # children: List['CategoryOut'] = [] # Cyclic reference handling needed if we want tree structure in one go
