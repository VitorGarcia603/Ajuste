"""create produtos, lotes, movimentacoes tables

Revision ID: 0001_initial
Revises: 
Create Date: 2025-04-29

"""

from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'produtos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(length=120), nullable=False, unique=True),
        sa.Column('estoque_min', sa.Integer(), nullable=True),
        sa.Column('estoque_atual', sa.Integer(), nullable=True),
        sa.Column('custo_medio', sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
        sa.Column('atualizado_em', sa.DateTime(), nullable=True),
    )
    op.create_table(
        'lotes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('produto_id', sa.Integer(), nullable=False),
        sa.Column('qtd_disponivel', sa.Integer(), nullable=True),
        sa.Column('custo_unit', sa.Numeric(precision=12, scale=2)),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['produto_id'], ['produtos.id']),
    )
    op.create_table(
        'movimentacoes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('produto_id', sa.Integer(), nullable=False),
        sa.Column('tipo', sa.Enum('ENTRADA','SAIDA','AJUSTE', name='tipomov'), nullable=False),
        sa.Column('qtd', sa.Integer(), nullable=True),
        sa.Column('custo_unit', sa.Numeric(precision=12, scale=2)),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['produto_id'], ['produtos.id']),
    )

def downgrade():
    op.drop_table('movimentacoes')
    op.drop_table('lotes')
    op.drop_table('produtos')
    op.execute('DROP TYPE IF EXISTS tipomov')