"""new_information.

Revision ID: f745d9545c1b
Revises: 148573858385
Create Date: 2023-12-21 12:24:22.839952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f745d9545c1b'
down_revision = '148573858385'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('repair_information', schema=None) as batch_op:
        batch_op.add_column(sa.Column('brief_information', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('repair_information', schema=None) as batch_op:
        batch_op.drop_column('brief_information')

    # ### end Alembic commands ###
