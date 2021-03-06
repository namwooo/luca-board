"""create Board model

Revision ID: fef0b6e1d1a0
Revises: d6b07fda2143
Create Date: 2019-01-23 15:05:16.693058

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fef0b6e1d1a0'
down_revision = 'd6b07fda2143'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('writer_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(240), nullable=True),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['writer_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('board')
    # ### end Alembic commands ###
