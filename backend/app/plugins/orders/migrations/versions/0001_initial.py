"""initial schema for orders"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("note", sa.String(length=255), nullable=True),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_orders_tenant_id", "orders", ["tenant_id"], unique=False)
    op.create_index(
        "ix_orders_tenant_created", "orders", ["tenant_id", "created_at"], unique=False
    )

    op.create_table(
        "order_line",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("order_id", sa.String(length=36), nullable=False),
        sa.Column("product_id", sa.String(length=36), nullable=True),
        sa.Column("variant_id", sa.String(length=36), nullable=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("line_total", sa.Numeric(12, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_order_line_tenant_id", "order_line", ["tenant_id"], unique=False)
    op.create_index(
        "ix_order_line_tenant_order",
        "order_line",
        ["tenant_id", "order_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_order_line_tenant_order", table_name="order_line")
    op.drop_index("ix_order_line_tenant_id", table_name="order_line")
    op.drop_table("order_line")

    op.drop_index("ix_orders_tenant_created", table_name="orders")
    op.drop_index("ix_orders_tenant_id", table_name="orders")
    op.drop_table("orders")
