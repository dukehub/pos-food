"""initial schema for devices"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("device"):
        op.create_table(
            "device",
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("tenant_id", sa.String(length=36), nullable=False),
            sa.Column("name", sa.String(length=100), nullable=False),
            sa.Column("device_type", sa.String(length=32), nullable=False),
            sa.Column("identifier", sa.String(length=120), nullable=True),
            sa.Column("location", sa.String(length=120), nullable=True),
            sa.Column("ip_address", sa.String(length=64), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_device_tenant_id", "device", ["tenant_id"], unique=False)
        op.create_index("ix_device_tenant_name", "device", ["tenant_id", "name"], unique=False)
        op.create_index(
            "ix_device_tenant_type", "device", ["tenant_id", "device_type"], unique=False
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table("device"):
        op.drop_index("ix_device_tenant_type", table_name="device")
        op.drop_index("ix_device_tenant_name", table_name="device")
        op.drop_index("ix_device_tenant_id", table_name="device")
        op.drop_table("device")

