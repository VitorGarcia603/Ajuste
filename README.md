# App Ajuste — Sprint D2‑D4

Projeto Flask + SQLAlchemy 2.0 para módulo Produtos & Estoque.

## Como rodar

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
export FLASK_APP=app:create_app
flask db upgrade        # aplica migrations
flask run
```

Visite `http://localhost:5000/api/docs` para Swagger UI.