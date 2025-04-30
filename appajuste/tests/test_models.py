from decimal import Decimal
from app.models import Produto, TipoMov
from app.services import registrar_mov

def test_custo_medio(db_session):
    p = Produto(nome="HDMI 2m", estoque_min=5)
    db_session.add(p)
    db_session.commit()

    registrar_mov(db_session, p, {"tipo": TipoMov.ENTRADA, "qtd": 10, "custo_unit": Decimal('10')})
    registrar_mov(db_session, p, {"tipo": TipoMov.ENTRADA, "qtd": 10, "custo_unit": Decimal('14')})
    assert p.custo_medio == Decimal('12')

    registrar_mov(db_session, p, {"tipo": TipoMov.SAIDA, "qtd": 18})
    assert p.abaixo_min