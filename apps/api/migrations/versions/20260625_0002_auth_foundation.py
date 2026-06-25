"""auth foundation

Revision ID: 20260625_0002
Revises: 20260523_0001
Create Date: 2026-06-25 00:00:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = "20260625_0002"
down_revision = "20260523_0001"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    existing_tables = set(inspect(bind).get_table_names())

    if "users" not in existing_tables:
        op.create_table(
            "users",
            sa.Column("id", sa.String(), nullable=False),
            sa.Column("primary_email", sa.String(), nullable=False),
            sa.Column("display_name", sa.String(), nullable=True),
            sa.Column("status", sa.String(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_users_primary_email"), "users", ["primary_email"], unique=True)
        op.create_index(op.f("ix_users_status"), "users", ["status"], unique=False)

    if "oauth_identities" not in existing_tables:
        op.create_table(
            "oauth_identities",
            sa.Column("id", sa.String(), nullable=False),
            sa.Column("user_id", sa.String(), nullable=False),
            sa.Column("provider", sa.String(), nullable=False),
            sa.Column("issuer", sa.String(), nullable=False),
            sa.Column("subject", sa.String(), nullable=False),
            sa.Column("email", sa.String(), nullable=True),
            sa.Column("email_verified", sa.Boolean(), nullable=False),
            sa.Column("claims_snapshot", sa.JSON(), nullable=True),
            sa.Column("last_seen_at", sa.DateTime(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("issuer", "subject", name="uq_oauth_identities_issuer_subject"),
        )
        op.create_index(op.f("ix_oauth_identities_issuer"), "oauth_identities", ["issuer"], unique=False)
        op.create_index(op.f("ix_oauth_identities_provider"), "oauth_identities", ["provider"], unique=False)
        op.create_index(op.f("ix_oauth_identities_subject"), "oauth_identities", ["subject"], unique=False)
        op.create_index(op.f("ix_oauth_identities_user_id"), "oauth_identities", ["user_id"], unique=False)

    if "account_memberships" not in existing_tables:
        op.create_table(
            "account_memberships",
            sa.Column("id", sa.String(), nullable=False),
            sa.Column("account_id", sa.String(), nullable=False),
            sa.Column("user_id", sa.String(), nullable=False),
            sa.Column("role", sa.String(), nullable=False),
            sa.Column("status", sa.String(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["account_id"], ["accounts.id"]),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("account_id", "user_id", name="uq_account_memberships_account_user"),
        )
        op.create_index(op.f("ix_account_memberships_account_id"), "account_memberships", ["account_id"], unique=False)
        op.create_index(op.f("ix_account_memberships_role"), "account_memberships", ["role"], unique=False)
        op.create_index(op.f("ix_account_memberships_status"), "account_memberships", ["status"], unique=False)
        op.create_index(op.f("ix_account_memberships_user_id"), "account_memberships", ["user_id"], unique=False)


def downgrade():
    bind = op.get_bind()
    existing_tables = set(inspect(bind).get_table_names())

    if "account_memberships" in existing_tables:
        op.drop_index(op.f("ix_account_memberships_user_id"), table_name="account_memberships")
        op.drop_index(op.f("ix_account_memberships_status"), table_name="account_memberships")
        op.drop_index(op.f("ix_account_memberships_role"), table_name="account_memberships")
        op.drop_index(op.f("ix_account_memberships_account_id"), table_name="account_memberships")
        op.drop_table("account_memberships")

    if "oauth_identities" in existing_tables:
        op.drop_index(op.f("ix_oauth_identities_user_id"), table_name="oauth_identities")
        op.drop_index(op.f("ix_oauth_identities_subject"), table_name="oauth_identities")
        op.drop_index(op.f("ix_oauth_identities_provider"), table_name="oauth_identities")
        op.drop_index(op.f("ix_oauth_identities_issuer"), table_name="oauth_identities")
        op.drop_table("oauth_identities")

    if "users" in existing_tables:
        op.drop_index(op.f("ix_users_status"), table_name="users")
        op.drop_index(op.f("ix_users_primary_email"), table_name="users")
        op.drop_table("users")
