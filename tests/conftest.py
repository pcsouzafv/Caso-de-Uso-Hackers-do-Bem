# task_manager/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config=None):
    app = Flask(__name__)
    
    # Configurações básicas
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///tasks.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'dev',
        'WTF_CSRF_ENABLED': True
    })
    
    # Aplica configurações customizadas se fornecidas
    if config:
        app.config.update(config)
    
    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)
    
    # Importa e registra blueprints
    from task_manager import routes
    app.register_blueprint(routes.bp)
    
    return app