"""create User Model

Revision ID: d6b07fda2143
Revises: 
Create Date: 2019-01-21 16:23:51.701608

"""
import sqlalchemy_utils
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy.dialects import mysql

revision = 'd6b07fda2143'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sqlalchemy_utils.types.email.EmailType(length=255), nullable=False),
                    sa.Column('password', sqlalchemy_utils.types.password.PasswordType(max_length=1024),
                              nullable=False),
                    sa.Column('first_name', sa.String(length=35), nullable=False),
                    sa.Column('last_name', sa.String(length=35), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False, default=False),
                    sa.Column('is_admin', sa.Boolean(), nullable=False, default=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    op.alter_column('user', 'is_admin',
                    existing_type=mysql.TINYINT(display_width=1),
                    type_=sa.Boolean(),
                    existing_nullable=False)
    op.alter_column('user', 'is_active',
                    existing_type=mysql.TINYINT(display_width=1),
                    type_=sa.Boolean(),
                    existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
