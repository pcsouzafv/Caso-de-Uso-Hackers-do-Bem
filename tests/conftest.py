import pytest
from typing import Generator, Any
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import User, Task, SystemLog
from config import TestConfig
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture
def test_app() -> Generator[Flask, None, None]:
    app.config.from_object(TestConfig)
    app.logger.setLevel(logging.DEBUG)
    
    with app.app_context():
        logger.debug("Criando banco de dados de teste")
        db.create_all()
        yield app
        logger.debug("Removendo banco de dados de teste")
        db.drop_all()

@pytest.fixture
def client(test_app: Flask) -> Generator[FlaskClient, None, None]:
    """Fixture que retorna um cliente de teste para a aplicação Flask."""
    return test_app.test_client()

@pytest.fixture
def test_user(test_app: Flask) -> Generator[User, None, None]:
    """Fixture que cria um usuário de teste."""
    with test_app.app_context():
        test_user = User(
            username='testuser',
            email='testuser@example.com',
            password_hash='testpass'
        )
        test_user.set_password('testpass')
        db.session.add(test_user)
        db.session.commit()
        logger.debug(f"Usuário de teste criado: {test_user.username}")
        yield test_user

@pytest.fixture
def test_task(test_app: Flask, test_user: User) -> Generator[Task, None, None]:
    """Fixture que cria uma tarefa de teste."""
    with test_app.app_context():
        task = Task(
            title='Test Task',
            description='Test description',
            user_id=test_user.id
        )
        db.session.add(task)
        db.session.commit()
        yield task

@pytest.fixture
def test_system_log(test_app: Flask, test_user: User) -> Generator[SystemLog, None, None]:
    """Fixture que cria um log de sistema de teste."""
    with test_app.app_context():
        log = SystemLog(
            action='Test action',
            user_id=test_user.id
        )
        db.session.add(log)
        db.session.commit()
        yield log