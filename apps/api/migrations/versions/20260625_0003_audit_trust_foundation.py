"""audit trust foundation

Revision ID: 20260625_0003
Revises: 20260625_0002
Create Date: 2026-06-25 00:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "20260625_0003"
down_revision = "20260625_0002"
branch_labels = None
depends_on = None


AUDIT_COLUMNS = {
    "actor_user_id": sa.Column("actor_user_id", sa.String(), nullable=True),
    "actor_identity_id": sa.Column("actor_identity_id", sa.String(), nullable=True),
    "auth_source": sa.Column("auth_source", sa.String(), nullable=True),
    "account_id": sa.Column("account_id", sa.String(), nullable=True),
    "object_type": sa.Column("object_type", sa.String(), nullable=True),
    "object_id": sa.Column("object_id", sa.String(), nullable=True),
    "route_template": sa.Column("route_template", sa.String(), nullable=True),
    "source_surface": sa.Column("source_surface", sa.String(), nullable=True),
    "decision": sa.Column("decision", sa.String(), nullable=True),
    "request_id": sa.Column("request_id", sa.String(), nullable=True),
    "event_context": sa.Column("event_context", sa.JSON(), nullable=True),
    "provenance_refs": sa.Column("provenance_refs", sa.JSON(), nullable=True),
}

INDEXED_COLUMNS = (
    "actor_user_id",
    "actor_identity_id",
    "auth_source",
    "account_id",
    "object_type",
    "object_id",
    "source_surface",
    "decision",
    "request_id",
)


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_tables = set(inspector.get_table_names())
    if "audit_events" not in existing_tables:
        return

    existing_columns = {column["name"] for column in inspector.get_columns("audit_events")}
    for column_name, column in AUDIT_COLUMNS.items():
        if column_name not in existing_columns:
            op.add_column("audit_events", column.copy())

    existing_indexes = {index["name"] for index in inspector.get_indexes("audit_events")}
    for column_name in INDEXED_COLUMNS:
        index_name = op.f(f"ix_audit_events_{column_name}")
        if index_name not in existing_indexes:
            op.create_index(index_name, "audit_events", [column_name], unique=False)


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_tables = set(inspector.get_table_names())
    if "audit_events" not in existing_tables:
        return

    existing_indexes = {index["name"] for index in inspector.get_indexes("audit_events")}
    for column_name in reversed(INDEXED_COLUMNS):
        index_name = op.f(f"ix_audit_events_{column_name}")
        if index_name in existing_indexes:
            op.drop_index(index_name, table_name="audit_events")

    existing_columns = {column["name"] for column in inspector.get_columns("audit_events")}
    for column_name in reversed(tuple(AUDIT_COLUMNS)):
        if column_name in existing_columns:
            op.drop_column("audit_events", column_name)
