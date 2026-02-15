"""initial schema for ticket_desingner"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ticket_template",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("template_type", sa.String(length=32), nullable=False),
        sa.Column("structure_json", sa.JSON(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_ticket_template_tenant_id", "ticket_template", ["tenant_id"], unique=False
    )
    op.create_index(
        "ix_ticket_template_tenant_name",
        "ticket_template",
        ["tenant_id", "name"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_ticket_template_tenant_name", table_name="ticket_template")
    op.drop_index("ix_ticket_template_tenant_id", table_name="ticket_template")
    op.drop_table("ticket_template")
