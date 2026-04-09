"""empty message

Revision ID: 45c58f4ceeec
Revises: 0506195b32d9
Create Date: 2026-04-10 02:48:10.899287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45c58f4ceeec'
down_revision: Union[str, Sequence[str], None] = '0506195b32d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Используем batch_alter_table для корректной работы с SQLite
    with op.batch_alter_table('auth_user', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'created_at',
                sa.DateTime(),
                server_default=sa.text('(CURRENT_TIMESTAMP)'),
                nullable=True
            )
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('auth_user', schema=None) as batch_op:
        batch_op.drop_column('created_at')