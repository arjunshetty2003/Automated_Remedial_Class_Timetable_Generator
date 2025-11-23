"""Add class organization structure

Revision ID: 20251123_195713
Revises:
Create Date: 2025-11-23 19:57:13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20251123_195713'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create classes table
    op.create_table('classes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('grade', sa.String(length=50), nullable=True),
        sa.Column('section', sa.String(length=50), nullable=True),
        sa.Column('academic_year', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_classes_id'), 'classes', ['id'], unique=False)

    # Add class_id to students table
    op.add_column('students', sa.Column('class_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_students_class_id'), 'students', ['class_id'], unique=False)
    op.create_foreign_key('fk_students_class_id', 'students', 'classes', ['class_id'], ['id'], ondelete='SET NULL')

    # Modify timetable table to support class-level schedules
    # Make student_id nullable
    op.alter_column('timetable', 'student_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # Add class_id column
    op.add_column('timetable', sa.Column('class_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_timetable_class_id'), 'timetable', ['class_id'], unique=False)
    op.create_foreign_key('fk_timetable_class_id', 'timetable', 'classes', ['class_id'], ['id'], ondelete='CASCADE')

    # Add subject column
    op.add_column('timetable', sa.Column('subject', sa.String(length=128), nullable=True))


def downgrade() -> None:
    # Remove subject column from timetable
    op.drop_column('timetable', 'subject')

    # Remove class_id from timetable
    op.drop_constraint('fk_timetable_class_id', 'timetable', type_='foreignkey')
    op.drop_index(op.f('ix_timetable_class_id'), table_name='timetable')
    op.drop_column('timetable', 'class_id')

    # Make student_id non-nullable again
    op.alter_column('timetable', 'student_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # Remove class_id from students
    op.drop_constraint('fk_students_class_id', 'students', type_='foreignkey')
    op.drop_index(op.f('ix_students_class_id'), table_name='students')
    op.drop_column('students', 'class_id')

    # Drop classes table
    op.drop_index(op.f('ix_classes_id'), table_name='classes')
    op.drop_table('classes')
