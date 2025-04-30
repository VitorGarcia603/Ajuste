from datetime import date
from typing import List

from flask import Blueprint, request, abort
from flask_login import current_user
from sqlalchemy import select
from app.extensions import db, spec
from app.finance.models import TituloFinanceiro, Parcela, Baixa
from app.finance.schemas import TituloCreate, BaixaDTO, TituloOut

bp_finance = Blueprint("finance", __name__, url_prefix="/api/v1/finance")


@bp_finance.get("/titulos")
@spec.validate(resp=List[TituloOut])
def list_titulos():
    q = select(TituloFinanceiro)
    tipo = request.args.get("tipo")
    if tipo:
        q = q.filter(TituloFinanceiro.tipo == tipo)
    titulos = db.session.scalars(q).all()
    return [TituloOut(**t.__dict__) for t in titulos], 200


@bp_finance.post("/titulos")
@spec.validate(body=TituloCreate, resp=TituloOut)
def create_titulo():
    data = request.context.body.dict()
    parcelas_json = data.pop("parcelas", [])
    titulo = TituloFinanceiro(**data, emissao_em=date.today())
    db.session.add(titulo)
    db.session.flush()

    if parcelas_json:
        for idx, p in enumerate(parcelas_json, start=1):
            db.session.add(
                Parcela(
                    titulo_id=titulo.id,
                    num=idx,
                    valor=p["valor"],
                    vencimento_em=p["vencimento_em"],
                    forma_pagto=p.get("forma_pagto"),
                )
            )
    else:
        db.session.add(
            Parcela(
                titulo_id=titulo.id,
                num=1,
                valor=titulo.valor_total,
                vencimento_em=titulo.vencimento_em,
            )
        )
    db.session.commit()
    return TituloOut(**titulo.__dict__), 201


@bp_finance.post("/parcelas/<int:pid>/baixa")
@spec.validate(body=BaixaDTO)
def baixa_parcela(pid):
    parcela = db.session.get(Parcela, pid)
    if not parcela:
        abort(404)
    dto = request.context.body

    baixa = Baixa(
        parcela_id=pid,
        valor_pago=dto.valor,
        pago_em=dto.pago_em or date.today(),
        juros=dto.juros,
        multa=dto.multa,
        desconto=dto.desconto,
        obs=dto.obs,
        user_id=current_user.id,
    )
    parcela.valor_pago += dto.valor
    db.session.add(baixa)
    db.session.commit()
    return {"message": "Baixa registrada."}, 201
