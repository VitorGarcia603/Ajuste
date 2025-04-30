import pandas as pd
from flask_smorest import Blueprint
from flask import request, jsonify
from ..db import db
from ..models import Produto
from ..schemas import ProdutoIn

bp = Blueprint("import_xlsx", __name__, url_prefix="/import", description="Importação de planilhas")

@bp.post("/xlsx")
def import_xlsx():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Envie um arquivo"}), 400
    df = pd.read_excel(file)

    try:
        produtos = [ProdutoIn(**row._asdict()) for row in df.itertuples(index=False)]
    except Exception as e:
        return jsonify({"errors": str(e)}), 400

    if request.args.get("preview") == "1":
        return jsonify([p.model_dump() for p in produtos])

    objs = [Produto(**p.model_dump()) for p in produtos]
    db.session.add_all(objs)
    db.session.commit()
    return "", 201