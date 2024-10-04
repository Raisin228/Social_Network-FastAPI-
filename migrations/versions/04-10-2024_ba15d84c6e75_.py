"""empty message

Revision ID: ba15d84c6e75
Revises: bc1af87f2e2a
Create Date: 2024-10-04 19:24:19.966803

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ba15d84c6e75"
down_revision: Union[str, None] = "bc1af87f2e2a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("uq_column1_column2_permuted", table_name="friend")
    op.create_index(
        "uq_user_id_friend_id_permuted",
        "friend",
        [
            sa.text("least(user_id, friend_id)"),
            sa.text("greatest(user_id, friend_id)"),
        ],
        unique=True,
    )
    op.drop_constraint("friend_friend_id_fkey", "friend", type_="foreignkey")
    op.drop_constraint("friend_user_id_fkey", "friend", type_="foreignkey")
    op.create_foreign_key(None, "friend", "user", ["user_id"], ["id"], ondelete="CASCADE")
    op.create_foreign_key(None, "friend", "user", ["friend_id"], ["id"], ondelete="CASCADE")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "friend", type_="foreignkey")
    op.drop_constraint(None, "friend", type_="foreignkey")
    op.create_foreign_key("friend_user_id_fkey", "friend", "user", ["user_id"], ["id"])
    op.create_foreign_key("friend_friend_id_fkey", "friend", "user", ["friend_id"], ["id"])
    op.drop_index("uq_user_id_friend_id_permuted", table_name="friend")
    op.create_index(
        "uq_column1_column2_permuted",
        "friend",
        [
            sa.text("LEAST(user_id, friend_id)"),
            sa.text("GREATEST(user_id, friend_id)"),
        ],
        unique=True,
    )
    # ### end Alembic commands ###
