from flask import Blueprint, render_template, request, jsonify, flash
from flask_login import login_required
from app.extensions import db
from app.models import Produto, MovimentoEstoque

estoque_bp = Blueprint("estoque", __name__, url_prefix="/estoque")

@estoque_bp.route("/")
@login_required
def estoque():
    categorias = db.session.query(Produto.categoria).distinct().all()
    return render_template("estoque.html", categorias=[c[0] for c in categorias])

@estoque_bp.route("/data")
@login_required
def estoque_data():
    draw  = int(request.args.get("draw", 1))
    start = int(request.args.get("start", 0))
    length = int(request.args.get("length", 10))
    search = request.args.get("search[value]", "")
    categoria = request.args.get("categoria", "")

    query = Produto.query
    if search:
        query = query.filter(Produto.nome.ilike(f"%{search}%"))
    if categoria:
        query = query.filter_by(categoria=categoria)

    total = query.count()
    produtos = query.order_by(Produto.id.desc()).offset(start).limit(length).all()

    data = [{
        "id": p.id,
        "nome": p.nome,
        "categoria": p.categoria,
        "estoque": p.estoque_atual,
        "custo": f"R$ {p.custo_unitario:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    } for p in produtos]

    return jsonify({"draw": draw, "recordsTotal": total,
                    "recordsFiltered": total, "data": data})

@estoque_bp.route("/movimentar", methods=["POST"])
@login_required
def movimentar():
    prod_id = int(request.form["prod_id"])
    tipo    = request.form["tipo"]
    qtd     = int(request.form["qtd"])
    custo   = float(request.form["custo"].replace(",", ".")) if tipo == "entrada" else 0

    produto = Produto.query.get_or_404(prod_id)
    if tipo == "entrada":
        produto.estoque_atual += qtd
        produto.custo_unitario = custo
    else:
        if qtd > produto.estoque_atual:
            flash("Estoque insuficiente!", "danger")
            return ("", 400)
        produto.estoque_atual -= qtd

    movimento = MovimentoEstoque(produto_id=prod_id, tipo=tipo,
                                 quantidade=qtd, custo_unitario=custo)
    db.session.add(movimento)
    db.session.commit()
    flash("Movimentação registrada!", "success")
    return ("", 204)
