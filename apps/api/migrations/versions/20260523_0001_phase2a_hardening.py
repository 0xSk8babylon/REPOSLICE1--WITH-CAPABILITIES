"""phase2a hardening baseline

Revision ID: 20260523_0001
Revises:
Create Date: 2026-05-23 00:00:00
"""

from alembic import op

from app.core import models  # noqa: F401
from app.core.database import Base

# revision identifiers, used by Alembic.
revision = "20260523_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade():
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)

