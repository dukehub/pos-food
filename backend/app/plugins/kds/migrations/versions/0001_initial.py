"""initial schema for kds"""

from alembic import op


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Compatibility checkpoint revision. Actual KDS schema is created in 0002_kds_initial.
    pass


def downgrade() -> None:
    # No-op to match upgrade behavior.
    pass
