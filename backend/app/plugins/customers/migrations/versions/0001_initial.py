"""initial schema for customers"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "customer",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("email", sa.String(length=160), nullable=True),
        sa.Column("nif", sa.String(length=64), nullable=True),
        sa.Column("ai", sa.String(length=64), nullable=True),
        sa.Column("rc", sa.String(length=64), nullable=True),
        sa.Column("tax_id", sa.String(length=64), nullable=True),
        sa.Column("address", sa.String(length=255), nullable=True),
        sa.Column("current_balance", sa.Numeric(12, 2), nullable=False),
        sa.Column("credit_limit", sa.Numeric(12, 2), nullable=True),
        sa.Column("payment_due_days", sa.Integer(), nullable=False),
        sa.Column("phone_whatsapp", sa.String(length=32), nullable=True),
        sa.Column("allow_notifications", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_customer_tenant_id", "customer", ["tenant_id"], unique=False)
    op.create_index(
        "ix_customer_tenant_name", "customer", ["tenant_id", "name"], unique=False
    )
    op.create_index(
        "ix_customer_tenant_phone", "customer", ["tenant_id", "phone"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_customer_tenant_phone", table_name="customer")
    op.drop_index("ix_customer_tenant_name", table_name="customer")
    op.drop_index("ix_customer_tenant_id", table_name="customer")
    op.drop_table("customer")
