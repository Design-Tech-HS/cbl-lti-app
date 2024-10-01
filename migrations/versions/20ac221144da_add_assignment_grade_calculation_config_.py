"""Add assignment_grade_calculation_config table

Revision ID: 20ac221144da
Revises: 1c1e86bba909
Create Date: 2024-08-04 16:13:23.606348

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20ac221144da'
down_revision = '1c1e86bba909'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignment_grade_calculation_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('canvas_assignment_id', sa.Integer(), nullable=False),
    sa.Column('do_not_drop', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('canvas_user_id', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['canvas_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assignment_grade_calculation_config')
    # ### end Alembic commands ###
