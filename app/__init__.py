from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializa o banco de dados
    db.init_app(app)
    
    # Inicializa o gerenciador de login
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Registra os blueprints
    from app import routes
    app.register_blueprint(routes.bp)
    
    return app

# Criação do app para uso direto (não recomendado para produção)
app = create_app(Config)
