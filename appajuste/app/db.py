from flask_sqlalchemy import SQLAlchemy
from contextlib import contextmanager

db = SQLAlchemy()

@contextmanager
def session_scope():
    session = db.session
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise