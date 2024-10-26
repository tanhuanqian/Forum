"""empty message

Revision ID: 8433e7d88992
Revises: 39f99b873a4c
Create Date: 2024-10-26 00:57:48.988827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8433e7d88992'
down_revision = '39f99b873a4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('comment_question_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'post_model', ['post_id'], ['id'])
        batch_op.drop_column('question_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('question_id', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('comment_question_id_fkey', 'post_model', ['question_id'], ['id'])
        batch_op.drop_column('post_id')

    # ### end Alembic commands ###
