from datetime import date, timedelta

from app.extensions import db
from app.finance.models import (
    TituloFinanceiro,
    Parcela,
    TipoTitulo,
    CategoriaFinanceira,
)


def test_titulo_saldo(session):
    cat = Category = CategoriaFinanceira(nome="Serviços", tipo=TipoTitulo.RECEBER)
    db.session.add(cat); db.session.flush()
    t = TituloFinanceiro(
        tipo=TipoTitulo.RECEBER,
        descricao="Fatura ABC",
        valor_total=1000,
        vencimento_em=date.today() + timedelta(days=30),
        categoria_id=cat.id,
    )
    db.session.add(t); db.session.flush()
    Parcela(
        titulo_id=t.id,
        num=1,
        valor=1000,
        vencimento_em=t.vencimento_em,
    )
    db.session.commit()
    assert t.saldo() == 1000
