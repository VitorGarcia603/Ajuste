# D5 – Orçamento ⇒ Pedido

### Passos rápidos
```bash
pip install -r requirements.txt
flask db upgrade
flask run
```

POST `/api/v1/vendas/orcamentos/<id>/aprovar` converte orçamento em pedido  
Baixa estoque, gera PDF e envia e‑mail usando SMTP de debug em `localhost:8025`.
