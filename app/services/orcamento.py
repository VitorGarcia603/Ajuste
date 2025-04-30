from app.db import db
from app.models.vendas import Orcamento, OrcamentoItem, HistoricoStatus
from app.utils.sequencial import gerar_numero
from app.services.pedido import PedidoService

MAX_DESCONTO = 15

class OrcamentoService:
    @staticmethod
    def create(cliente_nome, cliente_doc, validade, user_id):
        orc = Orcamento(
            numero=gerar_numero("ORC", Orcamento),
            cliente_nome=cliente_nome,
            cliente_doc=cliente_doc,
            validade=validade,
            criado_por=user_id,
        )
        db.session.add(orc); db.session.flush()
        OrcamentoService._log(orc, None, "RASCUNHO", user_id)
        return orc

    @staticmethod
    def add_item(orcamento, produto, qtd, preco_unit):
        OrcamentoItem(orcamento=orcamento, produto=produto,
                      qtd=qtd, preco_unit=preco_unit)
        orcamento.recomputar_total()

    @staticmethod
    def enviar(orcamento, user_id):
        OrcamentoService._transicionar(orcamento, "ENVIADO", user_id)

    @staticmethod
    def aprovar(orcamento, user_id):
        if orcamento.desconto_pct > MAX_DESCONTO:
            raise ValueError("Desconto acima do máximo permitido.")
        OrcamentoService._transicionar(orcamento, "APROVADO", user_id)
        return PedidoService.criar_de_orcamento(orcamento, user_id)

    # helpers
    @staticmethod
    def _transicionar(orcamento, novo_status, user_id):
        status_ant = orcamento.status
        orcamento.status = novo_status
        OrcamentoService._log(orcamento, status_ant, novo_status, user_id)

    @staticmethod
    def _log(ent, ant, novo, user):
        HistoricoStatus(tipo="ORCAMENTO", ref_id=ent.id,
                        status_ant=ant, status_novo=novo,
                        mudado_por=user)
