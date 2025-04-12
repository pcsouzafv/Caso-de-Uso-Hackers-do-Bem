from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./taskmanager.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Mantenho o SQLAlchemy para compatibilidade com a aplicação Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Inicializa a extensão SQLAlchemy para uso com Flask
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
