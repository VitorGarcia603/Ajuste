from decimal import Decimal
from sqlalchemy.orm import Session
from .models import Produto, Lote, Movimentacao, TipoMov
from .db import db

def reduzir_lotes(session: Session, produto_id: int, qtd: int):
    lotes = session.query(Lote).filter_by(produto_id=produto_id).order_by(Lote.criado_em).all()
    for lote in lotes:
        if qtd <= 0:
            break
        if lote.qtd_disponivel <= qtd:
            qtd -= lote.qtd_disponivel
            session.delete(lote)
        else:
            lote.qtd_disponivel -= qtd
            qtd = 0

def registrar_mov(session: Session, produto: Produto, data: dict):
    tipo = data["tipo"]
    qtd = int(data["qtd"])
    custo = data.get("custo_unit")

    if tipo == TipoMov.ENTRADA:
        lote = Lote(produto_id=produto.id, qtd_disponivel=qtd, custo_unit=Decimal(custo or 0))
        session.add(lote)
        produto.estoque_atual += qtd

    elif tipo == TipoMov.SAIDA:
        if qtd > produto.estoque_atual:
            raise ValueError("Estoque insuficiente")
        produto.estoque_atual -= qtd
        reduzir_lotes(session, produto.id, qtd)

    else:  # AJUSTE
        produto.estoque_atual += qtd
        if qtd < 0:
            reduzir_lotes(session, produto.id, -qtd)
        elif qtd > 0:
            # cria lote para ajuste positivo sem custo
            lote = Lote(produto_id=produto.id, qtd_disponivel=qtd, custo_unit=Decimal(custo or 0))
            session.add(lote)

    mov = Movimentacao(produto_id=produto.id, tipo=tipo, qtd=qtd, custo_unit=custo)
    session.add(mov)
    produto.recalc_custo_medio(session)