from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from .models import User, db

# Inicializa as extensões antes de configurar o app
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializa o banco de dados
    db.init_app(app)
    
    # Inicializa o gerenciador de login
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    
    # Função para carregar usuário
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Registra os blueprints
    from .routes import bp
    app.register_blueprint(bp)
    
    return app

# Criação do app para uso direto (não recomendado para produção)
app = create_app(Config)
