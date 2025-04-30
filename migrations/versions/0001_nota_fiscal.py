"""empty heads

Revision ID: 0001
Revises: 
Create Date: 2025-04-29 22:49:45

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'nota_fiscal',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('pedido_id', sa.Integer(), nullable=False),
        sa.Column('numero', sa.Integer(), nullable=False),
        sa.Column('serie', sa.Integer(), default=1),
        sa.Column('ambiente', sa.String(length=10)),
        sa.Column('status', sa.String(length=12)),
        sa.Column('chave_acesso', sa.String(length=44)),
        sa.Column('xml_path', sa.String(length=255)),
        sa.Column('pdf_path', sa.String(length=255)),
        sa.Column('protocolo', sa.String(length=20)),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )

def downgrade():
    op.drop_table('nota_fiscal')
