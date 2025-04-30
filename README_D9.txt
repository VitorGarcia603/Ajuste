APP Ajuste - Drop-in NF-e Sandbox (D9)
======================================

Conteúdo
--------
- app/models/fiscal.py ............ Model NotaFiscal
- app/services/nfe_service.py ..... Geração XML, assinatura, DANFE PDF
- app/routes/fiscal.py ............ Blueprint /api/v1/fiscal
- migrations/versions/0001_* ...... Alembic migration
- tests/test_nfe.py ............... Smoke test

Instalando
----------
pip install -r requirements.txt   # você precisará montar o arquivo
flask db upgrade                  # cria tabela nota_fiscal
flask run                         # rodar a aplicação

Endpoint principal
------------------
POST /api/v1/fiscal/nfe/pedido/<id>   -> cria XML, assina, valida, gera DANFE e grava NotaFiscal
GET  /api/v1/fiscal/nfe/<nf_id>       -> baixa o PDF da DANFE

Variáveis de ambiente
---------------------
NFE_PFX_BASE64   Base64 do .pfx (opcional no sandbox)
NFE_PFX_PWD      Senha do certificado

MEDIA_ROOT       Pasta base onde serão gravados XML/PDF (default media/nfe)
