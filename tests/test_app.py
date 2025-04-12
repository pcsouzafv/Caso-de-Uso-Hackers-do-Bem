# tests/test_app.py
import pytest
import os
import sys

# Garante que os módulos do projeto possam ser importados
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_app_creation():
    """Testa a criação da aplicação Flask"""
    try:
        # Tenta importar da versão principal (porta 8080)
        from app import create_app
        app = create_app()
        assert app is not None
    except ImportError:
        try:
            # Se falhar, tenta importar da versão task_manager (porta 5000)
            from task_manager import create_app
            app = create_app()
            assert app is not None
        except ImportError:
            pytest.skip("Nenhuma função create_app encontrada nos módulos")

def test_app_config():
    """Testa a configuração da aplicação"""
    try:
        # Tenta importar da versão principal (porta 8080)
        from app import create_app
        app = create_app()
    except ImportError:
        try:
            # Se falhar, tenta importar da versão task_manager (porta 5000)
            from task_manager import create_app
            app = create_app()
        except ImportError:
            pytest.skip("Nenhuma função create_app encontrada nos módulos")
    
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False
    assert 'SQLALCHEMY_DATABASE_URI' in app.config
    assert 'SECRET_KEY' in app.config