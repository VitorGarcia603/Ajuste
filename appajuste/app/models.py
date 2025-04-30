from datetime import datetime
from decimal import Decimal
from enum import StrEnum, auto
from sqlalchemy import DateTime, Enum, Numeric, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import db

class TipoMov(StrEnum):
    ENTRADA = auto()
    SAIDA   = auto()
    AJUSTE  = auto()

class Produto(db.Model):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    estoque_min: Mapped[int] = mapped_column(default=0)
    estoque_atual: Mapped[int] = mapped_column(default=0)
    custo_medio: Mapped[Decimal] = mapped_column(Numeric(12,2), default=0)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    atualizado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    lotes: Mapped[list["Lote"]] = relationship(back_populates="produto", cascade="all, delete-orphan")
    movs:  Mapped[list["Movimentacao"]] = relationship(back_populates="produto", cascade="all, delete-orphan")

    def recalc_custo_medio(self, session):
        total_custo = session.execute(
            db.select(db.func.sum(Lote.qtd_disponivel * Lote.custo_unit)).filter(Lote.produto_id == self.id)
        ).scalar() or Decimal(0)
        total_qtd = session.execute(
            db.select(db.func.sum(Lote.qtd_disponivel)).filter(Lote.produto_id == self.id)
        ).scalar() or 0
        if total_qtd:
            self.custo_medio = total_custo / total_qtd

    @property
    def abaixo_min(self) -> bool:
        return self.estoque_atual < self.estoque_min


class Lote(db.Model):
    __tablename__ = "lotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"), nullable=False)
    qtd_disponivel: Mapped[int]
    custo_unit: Mapped[Decimal] = mapped_column(Numeric(12,2))
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    produto: Mapped["Produto"] = relationship(back_populates="lotes")


class Movimentacao(db.Model):
    __tablename__ = "movimentacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"), nullable=False)
    tipo: Mapped[TipoMov] = mapped_column(Enum(TipoMov), nullable=False)
    qtd: Mapped[int]
    custo_unit: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    produto: Mapped["Produto"] = relationship(back_populates="movs")