from flask_smorest import Blueprint, abort
from flask import request
from ..db import db
from ..models import Produto
from ..schemas import ProdutoIn, ProdutoOut

bp = Blueprint("produtos", __name__, url_prefix="/produtos", description="CRUD Produtos")

@bp.post("/", response=ProdutoOut, arguments={"json": ProdutoIn})
def criar(body: ProdutoIn):
    p = Produto(**body.model_dump())
    db.session.add(p)
    db.session.commit()
    return p

@bp.get("/", response=list[ProdutoOut])
def listar():
    return Produto.query.all()

@bp.get("/<int:pid>", response=ProdutoOut)
def detalhe(pid):
    p = Produto.query.get_or_404(pid)
    return p

@bp.put("/<int:pid>", response=ProdutoOut, arguments={"json": ProdutoIn})
def atualizar(pid, body: ProdutoIn):
    p = Produto.query.get_or_404(pid)
    data = body.model_dump()
    for k, v in data.items():
        setattr(p, k, v)
    db.session.commit()
    return p

@bp.delete("/<int:pid>")
def excluir(pid):
    p = Produto.query.get_or_404(pid)
    db.session.delete(p)
    db.session.commit()
    return "", 204