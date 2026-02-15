"""initial schema for invoices"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "invoice",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("number", sa.String(length=50), nullable=False),
        sa.Column("customer_id", sa.String(length=36), nullable=True),
        sa.Column("customer_name", sa.String(length=120), nullable=True),
        sa.Column("customer_tax_id", sa.String(length=64), nullable=True),
        sa.Column("customer_address", sa.String(length=255), nullable=True),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "number", name="uq_invoice_tenant_number"),
    )
    op.create_index("ix_invoice_tenant_id", "invoice", ["tenant_id"], unique=False)
    op.create_index(
        "ix_invoice_tenant_created", "invoice", ["tenant_id", "created_at"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_invoice_tenant_created", table_name="invoice")
    op.drop_index("ix_invoice_tenant_id", table_name="invoice")
    op.drop_table("invoice")
