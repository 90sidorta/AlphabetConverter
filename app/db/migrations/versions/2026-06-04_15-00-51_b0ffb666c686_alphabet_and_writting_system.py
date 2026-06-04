"""Alphabet And Writting System

Revision ID: b0ffb666c686
Revises:
Create Date: 2026-06-04 15:00:51.974761

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic
revision = 'b0ffb666c686'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'script_families',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True), nullable=False),
        sa.Column('date_modified', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_script_families')),
        sa.UniqueConstraint('name', name=op.f('uq_script_families_name'))
    )
    op.create_table(
        'alphabets',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('writting_system', sa.Enum('ALPHABET', 'ABJAD', 'ABUGIDA', 'SYLLABARY', 'LOGOGRAPHIC', 'MIXED', name='writtingsystem'), nullable=False),
        sa.Column('writting_direction', sa.Enum('RTL', 'LTR', 'TTB', name='writtingdirection'), nullable=False),
        sa.Column('script_family_id', sa.UUID(), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True), nullable=False),
        sa.Column('date_modified', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['script_family_id'], ['script_families.id'], name=op.f('fk_alphabets_script_family_id_script_families'), ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_alphabets'))
    )


def downgrade() -> None:
    op.drop_table('alphabets')
    op.drop_table('script_families')
