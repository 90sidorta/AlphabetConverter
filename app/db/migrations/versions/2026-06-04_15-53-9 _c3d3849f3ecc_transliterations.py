"""Transliterations

Revision ID: c3d3849f3ecc
Revises: 044f19abdd94
Create Date: 2026-06-04 15:53:09.764231

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic
revision = 'c3d3849f3ecc'
down_revision = '044f19abdd94'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'transliteration_systems',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('date_created', sa.DateTime(timezone=True), nullable=False),
        sa.Column('date_modified', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_transliteration_systems')),
        sa.UniqueConstraint('name', name=op.f('uq_transliteration_systems_name'))
    )
    op.create_table(
        'transliteration_characters',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('value', sa.String(), nullable=False),
        sa.Column('character_id', sa.UUID(), nullable=False),
        sa.Column('transliteration_system_id', sa.UUID(), nullable=False),
        sa.Column('date_created', sa.DateTime(timezone=True), nullable=False),
        sa.Column('date_modified', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ['character_id'],
            ['characters.id'],
            name=op.f('fk_transliteration_characters_character_id_characters'),
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['transliteration_system_id'],
            ['transliteration_systems.id'],
            name=op.f('fk_transliteration_characters_transliteration_system_id_transliteration_systems'),
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_transliteration_characters')),
        sa.UniqueConstraint('character_id', 'transliteration_system_id', name='uq_transliteration_characters_character_id_system_id')
    )


def downgrade() -> None:
    op.drop_table('transliteration_characters')
    op.drop_table('transliteration_systems')
