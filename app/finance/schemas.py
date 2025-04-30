from datetime import date
from typing import List, Literal
from pydantic import BaseModel, Field

class ParcelaCreate(BaseModel):
    valor: float
    vencimento_em: date
    forma_pagto: Literal["PIX", "BOLETO", "CARTAO"] | None = None

class TituloCreate(BaseModel):
    tipo: Literal["PAGAR", "RECEBER"]
    descricao: str
    valor_total: float
    vencimento_em: date
    categoria_id: int
    cliente_fornecedor: str | None = None
    parcelas: List[ParcelaCreate] = Field(default_factory=list)

class BaixaDTO(BaseModel):
    valor: float
    pago_em: date | None = None
    juros: float | None = 0
    multa: float | None = 0
    desconto: float | None = 0
    obs: str | None = None

class TituloOut(BaseModel):
    id: int
    tipo: str
    descricao: str
    valor_total: float
    status: str
