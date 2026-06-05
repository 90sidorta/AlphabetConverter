"""restrict deletions and uniqe alphabet names

Revision ID: fd2e930bfa6d
Revises: c3d3849f3ecc
Create Date: 2026-06-05 12:40:05.010221

"""
from alembic import op


# revision identifiers, used by Alembic
revision = 'fd2e930bfa6d'
down_revision = 'c3d3849f3ecc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(op.f('uq_alphabets_name'), 'alphabets', ['name'])
    op.drop_constraint(op.f('fk_characters_alphabet_id_alphabets'), 'characters', type_='foreignkey')
    op.create_foreign_key(op.f('fk_characters_alphabet_id_alphabets'), 'characters', 'alphabets', ['alphabet_id'], ['id'], ondelete='RESTRICT')


def downgrade() -> None:
    op.drop_constraint(op.f('fk_characters_alphabet_id_alphabets'), 'characters', type_='foreignkey')
    op.create_foreign_key(op.f('fk_characters_alphabet_id_alphabets'), 'characters', 'alphabets', ['alphabet_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(op.f('uq_alphabets_name'), 'alphabets', type_='unique')
