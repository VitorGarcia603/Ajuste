from flask import Flask
from flask_smorest import Api
from .db import db
from .api.produtos import bp as bp_prod
from .api.lotes import bp as bp_lote
from .api.movimentacoes import bp as bp_mov
from .api.import_xlsx import bp as bp_imp

def create_app():
    app = Flask(__name__)
    app.config["API_TITLE"] = "App Ajuste API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///appajuste.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)
    api = Api(app)
    api.register_blueprint(bp_prod)
    api.register_blueprint(bp_lote)
    api.register_blueprint(bp_mov)
    api.register_blueprint(bp_imp)
    return app