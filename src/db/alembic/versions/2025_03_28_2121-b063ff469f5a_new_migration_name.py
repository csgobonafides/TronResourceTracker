"""new_migration_name

Revision ID: b063ff469f5a
Revises: 
Create Date: 2025-03-28 21:21:33.813230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b063ff469f5a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wallet_info',
    sa.Column('wallet_address', sa.String(length=50), nullable=False),
    sa.Column('balance', sa.DECIMAL(precision=50, scale=10), nullable=False),
    sa.Column('bandwidth', sa.INTEGER(), nullable=False),
    sa.Column('energy', sa.INTEGER(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('create_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wallet_info')
    # ### end Alembic commands ###
