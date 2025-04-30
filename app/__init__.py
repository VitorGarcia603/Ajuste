from flask import Flask
from flask_login import LoginManager
from app.models import db, Usuario
import os
 
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'chave')
import os
basedir = os.path.abspath(os.path.dirname(__file__))   # aponta para a pasta app/
db_path = os.path.join(basedir, '..', 'instance', 'banco.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# carregar rotas
from app import main_routes 
