"""initial schema for config"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "restaurant_config",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("currency", sa.String(length=16), nullable=False),
        sa.Column("locale", sa.String(length=16), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(length=160), nullable=False),
        sa.Column("tax_nif", sa.String(length=64), nullable=False),
        sa.Column("tax_rc", sa.String(length=64), nullable=False),
        sa.Column("tax_ai", sa.String(length=64), nullable=False),
        sa.Column("logo_url", sa.String(length=255), nullable=False),
        sa.Column("background_image_url", sa.String(length=255), nullable=False),
        sa.Column("background_image_secondary_url", sa.String(length=255), nullable=False),
        sa.Column("location_label", sa.String(length=255), nullable=False),
        sa.Column("city", sa.String(length=120), nullable=False),
        sa.Column("country", sa.String(length=120), nullable=False),
        sa.Column("postal_code", sa.String(length=32), nullable=False),
        sa.Column("latitude", sa.String(length=32), nullable=False),
        sa.Column("longitude", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", name="uq_restaurant_config_tenant"),
    )
    op.create_index(
        "ix_restaurant_config_tenant_id", "restaurant_config", ["tenant_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_restaurant_config_tenant_id", table_name="restaurant_config")
    op.drop_table("restaurant_config")

