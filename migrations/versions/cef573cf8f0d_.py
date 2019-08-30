"""empty message

Revision ID: cef573cf8f0d
Revises: 
Create Date: 2019-08-29 08:40:03.998092

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cef573cf8f0d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'intro')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('intro', mysql.VARCHAR(length=50), nullable=True))
    # ### end Alembic commands ###