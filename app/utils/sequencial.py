from datetime import date
from app.db import db

def gerar_numero(prefixo: str, modelo):
    ano = date.today().year
    ultimo = (
        db.session.query(modelo)
        .filter(modelo.numero.like(f"{prefixo}-{ano}-%"))
        .order_by(modelo.numero.desc())
        .first()
    )
    seq = int(ultimo.numero.split("-")[-1]) + 1 if ultimo else 1
    return f"{prefixo}-{ano}-{seq:04d}"
