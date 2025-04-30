from datetime import datetime
from enum import Enum
from app.extensions import db

class Ambiente(str, Enum):
    HOMOLOG = "HOMOLOG"
    PROD    = "PROD"

class StatusNF(str, Enum):
    GERADA      = "GERADA"
    ENVIADA     = "ENVIADA"
    AUTORIZADA  = "AUTORIZADA"
    REJEITADA   = "REJEITADA"

class NotaFiscal(db.Model):
    __tablename__ = "nota_fiscal"

    id            = db.Column(db.Integer, primary_key=True)
    pedido_id     = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    numero        = db.Column(db.Integer, nullable=False)
    serie         = db.Column(db.Integer, default=1)
    ambiente      = db.Column(db.Enum(Ambiente), default=Ambiente.HOMOLOG)
    status        = db.Column(db.Enum(StatusNF), default=StatusNF.GERADA)
    chave_acesso  = db.Column(db.String(44))
    xml_path      = db.Column(db.String(255))
    pdf_path      = db.Column(db.String(255))
    protocolo     = db.Column(db.String(20))
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
