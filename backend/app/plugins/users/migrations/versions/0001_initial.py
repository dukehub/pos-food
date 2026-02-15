"""initial schema for users"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "staff_user",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=True),
        sa.Column("pin_code", sa.String(length=12), nullable=True),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("language", sa.String(length=10), nullable=False),
        sa.Column("avatar_url", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "tenant_id", "username", name="uq_staff_user_tenant_username"
        ),
    )
    op.create_index("ix_staff_user_tenant_id", "staff_user", ["tenant_id"], unique=False)
    op.create_index(
        "ix_staff_user_tenant_role", "staff_user", ["tenant_id", "role"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_staff_user_tenant_role", table_name="staff_user")
    op.drop_index("ix_staff_user_tenant_id", table_name="staff_user")
    op.drop_table("staff_user")
