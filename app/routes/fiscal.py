from flask import Blueprint, jsonify, send_file, abort
from flask_login import login_required
from app.extensions import db
from app.models.fiscal import NotaFiscal
from app.services.nfe_service import gerar_xml, assinar_xml, validar_xml, gerar_danfe
from app.models import Pedido

bp_fiscal = Blueprint("fiscal", __name__, url_prefix="/api/v1/fiscal")

@bp_fiscal.route("/nfe/pedido/<int:pedido_id>", methods=["POST"])
@login_required
def criar_nfe(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    xml_path = gerar_xml(pedido)
    assinar_xml(xml_path)
    errors = validar_xml(xml_path)
    if errors:
        abort(422, "\n".join(errors))
    pdf_path = gerar_danfe(xml_path)
    nf = NotaFiscal(
        pedido_id=pedido.id,
        numero=pedido.id,
        xml_path=str(xml_path),
        pdf_path=str(pdf_path)
    )
    db.session.add(nf)
    db.session.commit()
    return jsonify({"nf_id": nf.id, "pdf": f"/api/v1/fiscal/nfe/{nf.id}"}), 201

@bp_fiscal.route("/nfe/<int:nf_id>", methods=["GET"])
@login_required
def baixar_pdf(nf_id):
    nf = NotaFiscal.query.get_or_404(nf_id)
    return send_file(nf.pdf_path, as_attachment=True)
