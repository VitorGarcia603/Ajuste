from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field, PositiveInt
from enum import Enum

class TipoMov(str, Enum):
    ENTRADA = "ENTRADA"
    SAIDA   = "SAIDA"
    AJUSTE  = "AJUSTE"

class ProdutoIn(BaseModel):
    nome: str = Field(..., max_length=120)
    estoque_min: int = 0

class ProdutoOut(ProdutoIn):
    id: int
    estoque_atual: int
    custo_medio: Decimal
    abaixo_min: bool
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}

class MovIn(BaseModel):
    produto_id: int
    tipo: TipoMov
    qtd: PositiveInt
    custo_unit: Decimal | None = None

class MovOut(MovIn):
    id: int
    criado_em: datetime

    model_config = {"from_attributes": True}