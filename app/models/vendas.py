from __future__ import annotations
from datetime import datetime, date
from typing import Literal
from sqlalchemy import Index, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, validates
from app.db import db

StatusOrc = Literal["RASCUNHO", "ENVIADO", "APROVADO", "EXPIRADO"]
StatusPed = Literal["ABERTO", "FATURADO", "CANCELADO"]

class Base(DeclarativeBase):
    pass

class Orcamento(Base):
    __tablename__ = "orcamentos"
    id: Mapped[int] = mapped_column(primary_key=True)
    numero: Mapped[str] = mapped_column(String(20), unique=True)
    cliente_nome: Mapped[str] = mapped_column(String(120))
    cliente_doc: Mapped[str] = mapped_column(String(20))
    data: Mapped[date] = mapped_column(default=date.today)
    status: Mapped[StatusOrc] = mapped_column(default="RASCUNHO")
    desconto_pct: Mapped[float] = mapped_column(default=0)
    validade: Mapped[date]
    total: Mapped[float] = mapped_column(default=0)
    criado_por: Mapped[int]

    itens: Mapped[list["OrcamentoItem"]] = relationship(
        back_populates="orcamento", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_orc_status_data", "status", "data"),
    )

    def recomputar_total(self):
        self.total = sum(it.subtotal for it in self.itens) * (1 - self.desconto_pct/100)

class OrcamentoItem(Base):
    __tablename__ = "orcamento_itens"
    id: Mapped[int] = mapped_column(primary_key=True)
    orcamento_id: Mapped[int] = mapped_column(ForeignKey("orcamentos.id"))
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    qtd: Mapped[int]
    preco_unit: Mapped[float]
    subtotal: Mapped[float]

    orcamento: Mapped[Orcamento] = relationship(back_populates="itens")
    produto = relationship("Produto")

    @validates("qtd", "preco_unit")
    def _recalc(self, key, value):
        setattr(self, key, value)
        self.subtotal = self.qtd * self.preco_unit
        return value

class Pedido(Base):
    __tablename__ = "pedidos"
    id: Mapped[int] = mapped_column(primary_key=True)
    numero: Mapped[str] = mapped_column(String(20), unique=True)
    orcamento_id: Mapped[int] = mapped_column(ForeignKey("orcamentos.id"))
    cliente_nome: Mapped[str]
    cliente_doc: Mapped[str]
    data: Mapped[date] = mapped_column(default=date.today)
    total: Mapped[float]
    status: Mapped[StatusPed] = mapped_column(default="ABERTO")
    criado_por: Mapped[int]

    itens: Mapped[list["PedidoItem"]] = relationship(
        back_populates="pedido", cascade="all, delete-orphan"
    )
    orcamento = relationship("Orcamento")

class PedidoItem(Base):
    __tablename__ = "pedido_itens"
    id: Mapped[int] = mapped_column(primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"))
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    qtd: Mapped[int]
    preco_unit: Mapped[float]
    subtotal: Mapped[float]

    pedido: Mapped[Pedido] = relationship(back_populates="itens")
    produto = relationship("Produto")

class HistoricoStatus(Base):
    __tablename__ = "historicos_status"
    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[Literal["ORCAMENTO", "PEDIDO"]]
    ref_id: Mapped[int]
    status_ant: Mapped[str]
    status_novo: Mapped[str]
    mudado_por: Mapped[int]
    mudado_em: Mapped[datetime] = mapped_column(default=datetime.utcnow)
