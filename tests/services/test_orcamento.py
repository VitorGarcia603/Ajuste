import pytest
from app.services.orcamento import OrcamentoService

def test_aprovar_estouro_desconto(session, orc_factory):
    orc = orc_factory(desconto_pct=25)
    with pytest.raises(ValueError):
        OrcamentoService.aprovar(orc, user_id=1)
