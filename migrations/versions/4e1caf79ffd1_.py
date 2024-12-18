"""empty message

Revision ID: 4e1caf79ffd1
Revises: 8433e7d88992
Create Date: 2024-10-26 01:28:39.898406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e1caf79ffd1'
down_revision = '8433e7d88992'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vote_count', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post_model', schema=None) as batch_op:
        batch_op.drop_column('vote_count')

    # ### end Alembic commands ###
