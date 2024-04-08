"""empty message Revision ID: b6f1f3696338 Revises: 354ffb16381d Create Date: 2024-04-03 18:41:32.069889 """

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import cast

# revision identifiers, used by Alembic.
revision: str = "b6f1f3696338"
down_revision: Union[str, None] = "354ffb16381d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("temperature") as batch_op:
        batch_op.alter_column(
            "date", type_=sa.Date(), existing_type=sa.DATETIME(), nullable=False
        )
        batch_op.execute("UPDATE temperature SET date = DATE(date)")


def downgrade() -> None:
    with op.batch_alter_table("temperature") as batch_op:
        batch_op.alter_column(
            "date", type_=sa.DATETIME(), existing_type=sa.Date(), nullable=False
        )
        batch_op.execute("UPDATE temperature SET date = DATETIME(date)")
