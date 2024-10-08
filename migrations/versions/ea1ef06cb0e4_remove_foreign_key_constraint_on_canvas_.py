"""Remove foreign key constraint on canvas_user_id to prevent it being truncated

Revision ID: ea1ef06cb0e4
Revises: e116c56474a2
Create Date: 2024-08-22 17:25:29.145075

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea1ef06cb0e4'
down_revision = 'e116c56474a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('assignment_grade_calculation_config_canvas_user_id_fkey', 'assignment_grade_calculation_config', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('assignment_grade_calculation_config_canvas_user_id_fkey', 'assignment_grade_calculation_config', 'users', ['canvas_user_id'], ['id'])
    # ### end Alembic commands ###
