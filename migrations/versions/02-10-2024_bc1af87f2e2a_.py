"""empty message

Revision ID: bc1af87f2e2a
Revises: 132d302d2f78
Create Date: 2024-10-02 16:16:15.725391

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bc1af87f2e2a"
down_revision: Union[str, None] = "132d302d2f78"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "friend",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("friend_id", sa.UUID(), nullable=False),
        sa.Column(
            "relationship_type",
            sa.String(length=11),
            server_default="NOT_APPROVE",
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["friend_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "friend_id"),
    )
    op.create_index(
        "uq_column1_column2_permuted",
        "friend",
        [
            sa.text("least(user_id, friend_id)"),
            sa.text("greatest(user_id, friend_id)"),
        ],
        unique=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("uq_column1_column2_permuted", table_name="friend")
    op.drop_table("friend")
    # ### end Alembic commands ###