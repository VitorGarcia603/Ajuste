from app import app
from app.models import db, Usuario

with app.app_context():
    db.drop_all()
    db.create_all()
    # Crear usuário admin
    admin = Usuario(email='admin@teste.com', senha='123')
    db.session.add(admin)
    db.session.commit()
    print('Banco criado e usuário admin cadastrado!')