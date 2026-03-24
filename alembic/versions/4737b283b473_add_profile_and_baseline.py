"""Baseline schema (idempotent): users, tags, posts, post_tags, comments, profiles.

Revision ID: 4737b283b473
Revises:
Create Date: 2026-03-24 13:12:35.576794

Safe on empty databases and on existing installs that already have some tables
(e.g. created previously with metadata.create_all). Keeps revision id so
alembic_version rows already at 4737b283b473 remain valid.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "4737b283b473"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _tables(conn) -> set[str]:
    return set(sa.inspect(conn).get_table_names())


def upgrade() -> None:
    conn = op.get_bind()
    tables = _tables(conn)

    if "users" not in tables:
        op.create_table(
            "users",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("username", sa.String(length=50), nullable=False),
            sa.Column("email", sa.String(length=100), nullable=False),
            sa.Column("hashed_password", sa.String(length=255), nullable=False),
            sa.Column("full_name", sa.String(length=100), nullable=True),
            sa.Column(
                "is_active",
                sa.Boolean(),
                server_default=sa.text("1"),
                nullable=False,
            ),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("username"),
            sa.UniqueConstraint("email"),
        )
        op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
        op.create_index(op.f("ix_users_username"), "users", ["username"], unique=False)
        op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
        tables = _tables(conn)

    if "tags" not in tables:
        op.create_table(
            "tags",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("name", sa.String(length=50), nullable=False),
            sa.Column("description", sa.String(length=200), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("name"),
        )
        op.create_index(op.f("ix_tags_id"), "tags", ["id"], unique=False)
        op.create_index(op.f("ix_tags_name"), "tags", ["name"], unique=False)
        tables = _tables(conn)

    if "posts" not in tables:
        op.create_table(
            "posts",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("title", sa.String(length=200), nullable=False),
            sa.Column("slug", sa.String(length=200), nullable=False),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("summary", sa.String(length=500), nullable=True),
            sa.Column("author_id", sa.Integer(), nullable=False),
            sa.Column(
                "is_published",
                sa.Boolean(),
                server_default=sa.text("0"),
                nullable=False,
            ),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(["author_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("slug"),
        )
        op.create_index(op.f("ix_posts_id"), "posts", ["id"], unique=False)
        op.create_index(op.f("ix_posts_title"), "posts", ["title"], unique=False)
        op.create_index(op.f("ix_posts_slug"), "posts", ["slug"], unique=False)
        tables = _tables(conn)

    if "post_tags" not in tables:
        op.create_table(
            "post_tags",
            sa.Column("post_id", sa.Integer(), nullable=False),
            sa.Column("tag_id", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
            sa.ForeignKeyConstraint(["tag_id"], ["tags.id"]),
            sa.PrimaryKeyConstraint("post_id", "tag_id"),
        )
        tables = _tables(conn)

    if "comments" not in tables:
        op.create_table(
            "comments",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("content", sa.Text(), nullable=False),
            sa.Column("author_name", sa.String(length=100), nullable=False),
            sa.Column("author_email", sa.String(length=100), nullable=True),
            sa.Column("post_id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=True),
            sa.Column("parent_id", sa.Integer(), nullable=True),
            sa.Column(
                "is_approved",
                sa.String(length=20),
                server_default=sa.text("'pending'"),
                nullable=False,
            ),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(["parent_id"], ["comments.id"]),
            sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_comments_id"), "comments", ["id"], unique=False)
        tables = _tables(conn)

    if "profiles" not in tables:
        op.create_table(
            "profiles",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("bio", sa.Text(), nullable=True),
            sa.Column("avatar_url", sa.String(length=500), nullable=True),
            sa.Column("website", sa.String(length=255), nullable=True),
            sa.Column("location", sa.String(length=100), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("(CURRENT_TIMESTAMP)"),
                nullable=False,
            ),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("user_id"),
        )
        op.create_index(op.f("ix_profiles_id"), "profiles", ["id"], unique=False)
        tables = _tables(conn)

    if "users" in _tables(conn) and "profiles" in _tables(conn):
        op.execute(
            sa.text(
                """
                INSERT INTO profiles (user_id)
                SELECT u.id FROM users u
                WHERE NOT EXISTS (SELECT 1 FROM profiles p WHERE p.user_id = u.id)
                """
            )
        )


def downgrade() -> None:
    op.drop_table("profiles", if_exists=True)
    op.drop_table("comments", if_exists=True)
    op.drop_table("post_tags", if_exists=True)
    op.drop_table("posts", if_exists=True)
    op.drop_table("tags", if_exists=True)
    op.drop_table("users", if_exists=True)
