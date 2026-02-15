"""initial schema for product_bundle"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product_bundle_item",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("parent_product_id", sa.String(length=36), nullable=False),
        sa.Column("child_product_id", sa.String(length=36), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tenant_id",
            "parent_product_id",
            "child_product_id",
            name="uq_product_bundle_item_pair",
        ),
    )
    op.create_index(
        "ix_product_bundle_item_tenant_id",
        "product_bundle_item",
        ["tenant_id"],
        unique=False,
    )
    op.create_index(
        "ix_product_bundle_item_tenant_parent",
        "product_bundle_item",
        ["tenant_id", "parent_product_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_product_bundle_item_tenant_parent", table_name="product_bundle_item"
    )
    op.drop_index("ix_product_bundle_item_tenant_id", table_name="product_bundle_item")
    op.drop_table("product_bundle_item")
