from datetime import date
from enum import Enum, auto

from sqlalchemy import String, ForeignKey, Enum as PgEnum, Index, event
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.extensions import db


class TipoTitulo(Enum):
    PAGAR = auto()
    RECEBER = auto()


class StatusTitulo(Enum):
    ABERTO = auto()
    PARCIAL = auto()
    PAGO = auto()


class StatusParcela(Enum):
    ABERTO = auto()
    ATRASADO = auto()
    PAGO = auto()


class FormaPagamento(Enum):
    PIX = auto()
    BOLETO = auto()
    CARTAO = auto()


class CategoriaFinanceira(db.Model):
    __tablename__ = "categoria_financeira"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    tipo: Mapped[TipoTitulo] = mapped_column(PgEnum(TipoTitulo), nullable=False)
    cor_hex: Mapped[str | None] = mapped_column(String(7))


class TituloFinanceiro(db.Model):
    __tablename__ = "titulo_financeiro"
    __table_args__ = (
        Index("ix_titulo_tipo_venc", "tipo", "vencimento_em"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[TipoTitulo] = mapped_column(PgEnum(TipoTitulo), nullable=False)
    descricao: Mapped[str] = mapped_column(String(120))
    valor_total: Mapped[float]
    emissao_em: Mapped[date] = mapped_column(default=date.today)
    vencimento_em: Mapped[date]
    status: Mapped[StatusTitulo] = mapped_column(
        PgEnum(StatusTitulo), default=StatusTitulo.ABERTO, nullable=False
    )

    cliente_fornecedor: Mapped[str | None] = mapped_column(String(120))
    pedido_id: Mapped[int | None] = mapped_column(index=True)
    criado_por: Mapped[int | None] = mapped_column(index=True)

    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categoria_financeira.id"), nullable=False
    )
    categoria = relationship("CategoriaFinanceira")
    parcelas = relationship("Parcela", back_populates="titulo", cascade="all, delete-orphan")

    def saldo(self) -> float:
        return round(self.valor_total - sum(p.valor_pago for p in self.parcelas), 2)


class Parcela(db.Model):
    __tablename__ = "parcela"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo_id: Mapped[int] = mapped_column(ForeignKey("titulo_financeiro.id"))
    num: Mapped[int]
    valor: Mapped[float]
    vencimento_em: Mapped[date]
    forma_pagto: Mapped[FormaPagamento | None] = mapped_column(PgEnum(FormaPagamento))

    pago_em: Mapped[date | None]
    valor_pago: Mapped[float] = mapped_column(default=0)
    status: Mapped[StatusParcela] = mapped_column(
        PgEnum(StatusParcela), default=StatusParcela.ABERTO
    )

    titulo = relationship("TituloFinanceiro", back_populates="parcelas")
    baixas = relationship("Baixa", back_populates="parcela", cascade="all, delete-orphan")


class Baixa(db.Model):
    __tablename__ = "baixa"

    id: Mapped[int] = mapped_column(primary_key=True)
    parcela_id: Mapped[int] = mapped_column(ForeignKey("parcela.id"))
    pago_em: Mapped[date] = mapped_column(default=date.today)
    valor_pago: Mapped[float]
    juros: Mapped[float] = mapped_column(default=0)
    multa: Mapped[float] = mapped_column(default=0)
    desconto: Mapped[float] = mapped_column(default=0)
    obs: Mapped[str | None] = mapped_column(String(120))
    user_id: Mapped[int | None]

    parcela = relationship("Parcela", back_populates="baixas")


@event.listens_for(Parcela, "after_insert")
@event.listens_for(Parcela, "after_update")
def _sync_parcela_status(mapper, connection, target: Parcela):  # noqa
    today = date.today()
    from app.finance.models import StatusParcela, StatusTitulo, Parcela, TituloFinanceiro
    new_status = (
        StatusParcela.PAGO
        if target.valor_pago >= target.valor
        else StatusParcela.ATRASADO
        if today > target.vencimento_em
        else StatusParcela.ABERTO
    )
    if target.status != new_status:
        connection.execute(
            Parcela.__table__.update()
            .where(Parcela.id == target.id)
            .values(status=new_status)
        )

    saldo_expr = db.select(db.func.sum(Parcela.valor - Parcela.valor_pago)).where(
        Parcela.titulo_id == target.titulo_id
    )
    open_conn = connection.execute(saldo_expr).scalar() or 0
    new_titulo_status = (
        StatusTitulo.PAGO
        if open_conn == 0
        else StatusTitulo.PARCIAL
        if open_conn < target.titulo.valor_total
        else StatusTitulo.ABERTO
    )
    connection.execute(
        TituloFinanceiro.__table__.update()
        .where(TituloFinanceiro.id == target.titulo_id)
        .values(status=new_titulo_status)
    )
