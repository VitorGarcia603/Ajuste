import pandas as pd
from app import app
from app.models import db, Produto

# Caminho para a planilha — verifique se está correto
planilha_path = 'PLANILHA ORÇAMENTOS.xlsx'

def importar_produtos():
    # Lê a aba ESTOQUE
    df = pd.read_excel(planilha_path, sheet_name='ESTOQUE')

    with app.app_context():
        for _, row in df.iterrows():
            # Nome do produto: pula linhas em branco
            nome = row.get('PRODUTO')
            if pd.isna(nome) or str(nome).strip() == '':
                continue

            # Categoria (pode ser None)
            categoria = row.get('CATEGORIA')
            if pd.isna(categoria):
                categoria = None

            # Preço de custo, default 0.0 se faltar
            custo_raw = row.get('CUSTO')
            preco_custo = float(custo_raw) if not pd.isna(custo_raw) else 0.0

            # Estoque (saldo), default 0 se faltar
            saldo_raw = row.get('SALDO')
            estoque = int(saldo_raw) if not pd.isna(saldo_raw) else 0

            # Cria e adiciona o produto
            produto = Produto(
                nome=nome,
                categoria=categoria,
                preco_custo=preco_custo,
                estoque=estoque
            )
            db.session.add(produto)

        db.session.commit()
        print("✅ Produtos importados com sucesso!")

if __name__ == '__main__':
    importar_produtos()
