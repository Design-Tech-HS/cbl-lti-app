"""Remove section information from CourseUserLink

Revision ID: 959b1bac53ab
Revises: 2cabdd3a2b61
Create Date: 2024-10-01 12:09:51.815553

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '959b1bac53ab'
down_revision = '2cabdd3a2b61'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('course_user_link', 'section_id')
    op.drop_column('course_user_link', 'section_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course_user_link', sa.Column('section_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('course_user_link', sa.Column('section_id', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
