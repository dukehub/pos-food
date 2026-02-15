"""initial schema for printer"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("device_printer"):
        op.create_table(
            "device_printer",
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("tenant_id", sa.String(length=36), nullable=False),
            sa.Column("name", sa.String(length=100), nullable=False),
            sa.Column("driver_type", sa.String(length=20), nullable=False),
            sa.Column("system_printer_name", sa.String(length=120), nullable=True),
            sa.Column("ip_address", sa.String(length=64), nullable=True),
            sa.Column("port", sa.Integer(), nullable=False),
            sa.Column("paper_width", sa.Integer(), nullable=False),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            "ix_device_printer_tenant_id", "device_printer", ["tenant_id"], unique=False
        )
        op.create_index(
            "ix_device_printer_tenant_name",
            "device_printer",
            ["tenant_id", "name"],
            unique=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table("device_printer"):
        op.drop_index("ix_device_printer_tenant_name", table_name="device_printer")
        op.drop_index("ix_device_printer_tenant_id", table_name="device_printer")
        op.drop_table("device_printer")

