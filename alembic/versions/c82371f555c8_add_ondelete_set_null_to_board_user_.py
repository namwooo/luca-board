"""add ondelete set null to board-user relationship

Revision ID: c82371f555c8
Revises: 4b5eb594c3e9
Create Date: 2019-03-05 10:43:10.321395

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c82371f555c8'
down_revision = '4b5eb594c3e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('board', 'writer_id',
                    existing_type=mysql.INTEGER(display_width=11),
                    nullable=True)
    op.drop_constraint('board_ibfk_1', 'board', type_='foreignkey')
    op.create_foreign_key(None, 'board', 'user', ['writer_id'], ['id'], ondelete='SET NULL')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'board', type_='foreignkey')
    op.create_foreign_key('board_ibfk_1', 'board', 'user', ['writer_id'], ['id'])
    op.alter_column('board', 'writer_id',
                    existing_type=mysql.INTEGER(display_width=11),
                    nullable=False)
    # ### end Alembic commands ###
