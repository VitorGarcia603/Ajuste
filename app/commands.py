from flask import current_app as app
from app.extensions import db
from app.finance.models import CategoriaFinanceira, TipoTitulo


@app.cli.command("seed_finance")
def seed_finance():
    if db.session.query(CategoriaFinanceira).first():
        print("Categorias já existem.")
        return
    categorias = [
        CategoriaFinanceira(nome="Fornecedores", tipo=TipoTitulo.PAGAR, cor_hex="#F44336"),
        CategoriaFinanceira(nome="Impostos", tipo=TipoTitulo.PAGAR, cor_hex="#FF9800"),
        CategoriaFinanceira(nome="Clientes", tipo=TipoTitulo.RECEBER, cor_hex="#4CAF50"),
    ]
    db.session.add_all(categorias)
    db.session.commit()
    print("Categorias financeiras criadas!")
