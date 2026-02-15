"""initial schema for floor_plan"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "floor_plan_zone",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "name", name="uq_floor_plan_zone_tenant_name"),
    )
    op.create_index(
        "ix_floor_plan_zone_tenant_id", "floor_plan_zone", ["tenant_id"], unique=False
    )
    op.create_index(
        "ix_floor_plan_zone_tenant_order",
        "floor_plan_zone",
        ["tenant_id", "display_order"],
        unique=False,
    )

    op.create_table(
        "floor_plan_table",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("zone_id", sa.String(length=36), nullable=True),
        sa.Column("code", sa.String(length=40), nullable=False),
        sa.Column("qr_code", sa.String(length=128), nullable=True),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("current_server_id", sa.String(length=36), nullable=True),
        sa.Column("parent_table_id", sa.String(length=36), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["zone_id"], ["floor_plan_zone.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "code", name="uq_floor_plan_table_tenant_code"),
    )
    op.create_index(
        "ix_floor_plan_table_tenant_id", "floor_plan_table", ["tenant_id"], unique=False
    )
    op.create_index(
        "ix_floor_plan_table_tenant_zone",
        "floor_plan_table",
        ["tenant_id", "zone_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_floor_plan_table_tenant_zone", table_name="floor_plan_table")
    op.drop_index("ix_floor_plan_table_tenant_id", table_name="floor_plan_table")
    op.drop_table("floor_plan_table")

    op.drop_index("ix_floor_plan_zone_tenant_order", table_name="floor_plan_zone")
    op.drop_index("ix_floor_plan_zone_tenant_id", table_name="floor_plan_zone")
    op.drop_table("floor_plan_zone")
