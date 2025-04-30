from flask_smorest import Blueprint, abort
from flask import request
from ..db import db
from ..models import Lote, Produto
from datetime import datetime
from pydantic import BaseModel, PositiveInt
from decimal import Decimal

class LoteIn(BaseModel):
    produto_id: int
    qtd_disponivel: PositiveInt
    custo_unit: Decimal

class LoteOut(LoteIn):
    id: int
    criado_em: datetime
    model_config = {"from_attributes": True}

bp = Blueprint("lotes", __name__, url_prefix="/lotes", description="CRUD Lotes")

@bp.post("/", response=LoteOut, arguments={"json": LoteIn})
def criar(body: LoteIn):
    if not Produto.query.get(body.produto_id):
        abort(404, message="Produto não encontrado")
    lote = Lote(**body.model_dump())
    db.session.add(lote)
    db.session.commit()
    return lote

@bp.get("/", response=list[LoteOut])
def listar():
    return Lote.query.all()

@bp.get("/<int:lid>", response=LoteOut)
def detalhe(lid):
    return Lote.query.get_or_404(lid)

@bp.delete("/<int:lid>")
def excluir(lid):
    lote = Lote.query.get_or_404(lid)
    db.session.delete(lote)
    db.session.commit()
    return "", 204