"""initial schema for app_settings"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "app_setting",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("scope", sa.String(length=20), nullable=False),
        sa.Column("module", sa.String(length=60), nullable=False),
        sa.Column("key", sa.String(length=120), nullable=False),
        sa.Column("value_json", sa.JSON(), nullable=False),
        sa.Column("value_type", sa.String(length=20), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tenant_id", "scope", "key", name="uq_app_setting_tenant_scope_key"
        ),
    )
    op.create_index("ix_app_setting_tenant", "app_setting", ["tenant_id"], unique=False)
    op.create_index(
        "ix_app_setting_tenant_module", "app_setting", ["tenant_id", "module"], unique=False
    )
    op.create_index(
        "ix_app_setting_tenant_scope", "app_setting", ["tenant_id", "scope"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_app_setting_tenant_scope", table_name="app_setting")
    op.drop_index("ix_app_setting_tenant_module", table_name="app_setting")
    op.drop_index("ix_app_setting_tenant", table_name="app_setting")
    op.drop_table("app_setting")
