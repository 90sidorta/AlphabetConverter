"""Alphabet characters

Revision ID: 044f19abdd94
Revises: b0ffb666c686
Create Date: 2026-06-04 15:43:08.977096

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic
revision = '044f19abdd94'
down_revision = 'b0ffb666c686'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'characters',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('alphabet_id', sa.UUID(), nullable=False),
        sa.Column('value', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('unit_type', sa.Enum('LETTER', 'SEQUENCE', 'PUNCTUATION', name='alphabetunittype'), nullable=False),
        sa.Column('unicode_codepoint', sa.String(), nullable=True),
        sa.Column('date_created', sa.DateTime(timezone=True), nullable=False),
        sa.Column('date_modified', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['alphabet_id'], ['alphabets.id'], name=op.f('fk_characters_alphabet_id_alphabets'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_characters')),
        sa.UniqueConstraint('alphabet_id', 'value', name='uq_characters_alphabet_id_value')
    )


def downgrade() -> None:
    op.drop_table('characters')
