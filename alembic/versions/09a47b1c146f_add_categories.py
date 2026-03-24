"""add_categories

Revision ID: 09a47b1c146f
Revises: 3f63689ee46a
Create Date: 2026-03-24 13:27:07.447280

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "09a47b1c146f"
down_revision: Union[str, Sequence[str], None] = "3f63689ee46a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    insp = sa.inspect(conn)
    tables = set(insp.get_table_names())

    if "categories" not in tables:
        op.create_table(
            "categories",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=100), nullable=False),
            sa.Column("slug", sa.String(length=120), nullable=False),
            sa.Column("description", sa.String(length=500), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_categories_id"), "categories", ["id"], unique=False)
        op.create_index(op.f("ix_categories_name"), "categories", ["name"], unique=True)
        op.create_index(op.f("ix_categories_slug"), "categories", ["slug"], unique=True)

    post_cols = {c["name"] for c in insp.get_columns("posts")}
    if "category_id" not in post_cols:
        with op.batch_alter_table("posts", schema=None) as batch_op:
            batch_op.add_column(sa.Column("category_id", sa.Integer(), nullable=True))
            batch_op.create_foreign_key(
                "fk_posts_category_id_categories",
                "categories",
                ["category_id"],
                ["id"],
                ondelete="SET NULL",
            )


def downgrade() -> None:
    conn = op.get_bind()
    insp = sa.inspect(conn)
    post_cols = {c["name"] for c in insp.get_columns("posts")}

    if "category_id" in post_cols:
        with op.batch_alter_table("posts", schema=None) as batch_op:
            batch_op.drop_constraint(
                "fk_posts_category_id_categories", type_="foreignkey"
            )
            batch_op.drop_column("category_id")

    if "categories" in insp.get_table_names():
        op.drop_index(op.f("ix_categories_slug"), table_name="categories")
        op.drop_index(op.f("ix_categories_name"), table_name="categories")
        op.drop_index(op.f("ix_categories_id"), table_name="categories")
        op.drop_table("categories")
