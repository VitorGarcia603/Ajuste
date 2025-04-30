from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=True)
    preco_custo = db.Column(db.Float, nullable=False)
    preco_venda_sugerido = db.Column(db.Float, nullable=True)
    estoque = db.Column(db.Integer, default=0)
    entradas = db.Column(db.Integer, default=0)
    saidas = db.Column(db.Integer, default=0)
    custo_total = db.Column(db.Float, default=0)
    preco_medio = db.Column(db.Float, default=0)
    peso = db.Column(db.Float, nullable=True)
    largura = db.Column(db.Float, nullable=True)
    altura = db.Column(db.Float, nullable=True)
    profundidade = db.Column(db.Float, nullable=True)
    ultima_atualizacao = db.Column(db.DateTime, default=datetime.utcnow)

    movimentacoes = db.relationship('MovimentacaoProduto', backref='produto', lazy=True)

class MovimentacaoProduto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10))
    quantidade = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.String(200), nullable=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)