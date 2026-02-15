import re

def normalize_text(value: str) -> str:
    return value.strip().lower()

class ProductAlias(Base):
    __tablename__ = "product_aliases"
    __table_args__ = (
        UniqueConstraint("tenant_id", "product_id", "locale", "alias_norm", name="uq_alias_tenant_prod_locale_norm"),
        Index("ix_alias_tenant_locale", "tenant_id", "locale"),
    )

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    locale = Column(String(16), nullable=False)       # ar-DZ / fr-DZ
    alias = Column(String(100), nullable=False)
    alias_norm = Column(Text, nullable=False)

    product = relationship("Product", backref="aliases")