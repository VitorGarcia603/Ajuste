from fastapi import HTTPException
from app.db import db
from app.models.vendas import Pedido, PedidoItem, HistoricoStatus
from app.models.estoque import Movimentacao
from app.utils.sequencial import gerar_numero

class PedidoService:
    @staticmethod
    def criar_de_orcamento(orcamento, user_id):
        insuf = [it for it in orcamento.itens if it.qtd > it.produto.qtd_estoque]
        if insuf:
            raise HTTPException(409, detail="Estoque insuficiente.")

        ped = Pedido(
            numero=gerar_numero("PED", Pedido),
            orcamento=orcamento,
            cliente_nome=orcamento.cliente_nome,
            cliente_doc=orcamento.cliente_doc,
            total=orcamento.total,
            criado_por=user_id,
        )

        for it in orcamento.itens:
            PedidoItem(pedido=ped, produto=it.produto,
                       qtd=it.qtd, preco_unit=it.preco_unit,
                       subtotal=it.subtotal)
            it.produto.qtd_estoque -= it.qtd
            Movimentacao(tipo="SAIDA", produto=it.produto,
                         quantidade=it.qtd, pedido=ped)

        PedidoService._log(ped, None, "ABERTO", user_id)
        return ped

    @staticmethod
    def _log(ent, ant, novo, user):
        HistoricoStatus(tipo="PEDIDO", ref_id=ent.id,
                        status_ant=ant, status_novo=novo,
                        mudado_por=user)
