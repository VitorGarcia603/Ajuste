from flask_smorest import Blueprint, abort
from ..db import db
from ..models import Produto
from ..schemas import MovIn, MovOut
from ..services import registrar_mov

bp = Blueprint("movs", __name__, url_prefix="/movimentacoes", description="Movimentações de estoque")

@bp.post("/", response=MovOut, arguments={"json": MovIn})
def criar(body: MovIn):
    produto = Produto.query.get(body.produto_id)
    if not produto:
        abort(404, message="Produto não encontrado")
    registrar_mov(db.session, produto, body.model_dump())
    db.session.commit()
    return produto.movs[-1]

@bp.get("/<int:mid>", response=MovOut)
def detalhe(mid):
    from ..models import Movimentacao
    return Movimentacao.query.get_or_404(mid)