"""empty message

Revision ID: 1c2ba32f1ec0
Revises: 
Create Date: 2019-05-23 17:10:50.765064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c2ba32f1ec0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('address', sa.String(), nullable=True))
    op.add_column('user', sa.Column('age', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('career', sa.String(), nullable=True))
    op.add_column('user', sa.Column('mail', sa.String(), nullable=True))
    op.add_column('user', sa.Column('mobile', sa.String(), nullable=True))
    op.add_column('user', sa.Column('qq', sa.String(), nullable=True))
    op.add_column('user', sa.Column('sex', sa.String(), nullable=True))
    op.drop_column('user', 'privatekey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('privatekey', sa.VARCHAR(), nullable=False))
    op.drop_column('user', 'sex')
    op.drop_column('user', 'qq')
    op.drop_column('user', 'mobile')
    op.drop_column('user', 'mail')
    op.drop_column('user', 'career')
    op.drop_column('user', 'age')
    op.drop_column('user', 'address')
    # ### end Alembic commands ###