"""kds schema for devices plugin"""

from alembic import op
import sqlalchemy as sa


revision = "0002_kds_initial"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if not inspector.has_table("device_kds"):
        op.create_table(
            "device_kds",
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("tenant_id", sa.String(length=36), nullable=False),
            sa.Column("name", sa.String(length=100), nullable=False),
            sa.Column("ip_address", sa.String(length=64), nullable=True),
            sa.Column("port", sa.Integer(), nullable=False),
            sa.Column("location", sa.String(length=120), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index("ix_device_kds_tenant_id", "device_kds", ["tenant_id"], unique=False)
        op.create_index(
            "ix_device_kds_tenant_name",
            "device_kds",
            ["tenant_id", "name"],
            unique=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table("device_kds"):
        op.drop_index("ix_device_kds_tenant_name", table_name="device_kds")
        op.drop_index("ix_device_kds_tenant_id", table_name="device_kds")
        op.drop_table("device_kds")

