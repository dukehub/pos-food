"""fix_plugin_runtime_schema

Revision ID: 2d3b55d5d5e2
Revises: a564f55fdea8
Create Date: 2026-02-07 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2d3b55d5d5e2"
down_revision: Union[str, None] = "a564f55fdea8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(inspector: sa.Inspector, table_name: str) -> bool:
    return table_name in inspector.get_table_names()


def _column_names(inspector: sa.Inspector, table_name: str) -> set[str]:
    return {col["name"] for col in inspector.get_columns(table_name)}


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _table_exists(inspector, "tenant_plugins"):
        tenant_plugins_columns = _column_names(inspector, "tenant_plugins")
        if "installed_version" not in tenant_plugins_columns:
            op.add_column("tenant_plugins", sa.Column("installed_version", sa.String(length=50), nullable=True))
        if "installed_at" not in tenant_plugins_columns:
            op.add_column("tenant_plugins", sa.Column("installed_at", sa.DateTime(timezone=True), nullable=True))

    if not _table_exists(inspector, "permissions"):
        op.create_table(
            "permissions",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("tenant_id", sa.String(length=120), nullable=False),
            sa.Column("code", sa.String(length=120), nullable=False),
            sa.Column("label", sa.String(length=200), nullable=False),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("tenant_id", "code", name="uq_permissions_tenant_code"),
        )
        op.create_index("ix_permissions_tenant_id", "permissions", ["tenant_id"], unique=False)
        op.create_index("ix_permissions_code", "permissions", ["code"], unique=False)
        return

    permissions_columns = _column_names(inspector, "permissions")
    if not {"tenant_id", "code"}.issubset(permissions_columns):
        return

    unique_constraints = inspector.get_unique_constraints("permissions")
    old_unique_on_code = [
        uc.get("name")
        for uc in unique_constraints
        if uc.get("column_names") == ["code"] and uc.get("name")
    ]
    for constraint_name in old_unique_on_code:
        with op.batch_alter_table("permissions") as batch_op:
            batch_op.drop_constraint(constraint_name, type_="unique")

    indexes = inspector.get_indexes("permissions")
    old_unique_index_on_code = [
        idx.get("name")
        for idx in indexes
        if idx.get("unique") and idx.get("column_names") == ["code"] and idx.get("name")
    ]
    for index_name in old_unique_index_on_code:
        op.drop_index(index_name, table_name="permissions")

    unique_constraints = inspector.get_unique_constraints("permissions")
    has_composite_unique = any(
        set(uc.get("column_names") or []) == {"tenant_id", "code"} for uc in unique_constraints
    )
    if not has_composite_unique:
        with op.batch_alter_table("permissions") as batch_op:
            batch_op.create_unique_constraint("uq_permissions_tenant_code", ["tenant_id", "code"])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _table_exists(inspector, "permissions"):
        op.drop_table("permissions")

    if _table_exists(inspector, "tenant_plugins"):
        tenant_plugins_columns = _column_names(inspector, "tenant_plugins")
        with op.batch_alter_table("tenant_plugins") as batch_op:
            if "installed_at" in tenant_plugins_columns:
                batch_op.drop_column("installed_at")
            if "installed_version" in tenant_plugins_columns:
                batch_op.drop_column("installed_version")
