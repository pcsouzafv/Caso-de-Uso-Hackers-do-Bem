import pytest
from typing import Generator
from flask import Flask
from flask.testing import FlaskClient
from app import app, db
from app.models import User, Task, SystemLog
from config import TestConfig
import logging
import os
import tempfile
import threading
import time

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def test_app() -> Generator[Flask, None, None]:
    """Fixture que configura o app de teste"""
    # Criar um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp()
    app.config.from_object(TestConfig)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.logger.setLevel(logging.DEBUG)
    
    with app.app_context():
        logger.debug("Criando banco de dados de teste")
        db.create_all()
        yield app
        logger.debug("Removendo banco de dados de teste")
        db.drop_all()
        os.close(db_fd)
        os.unlink(db_path)

@pytest.fixture(scope="module")
def client(test_app: Flask) -> Generator[FlaskClient, None, None]:
    """Fixture que retorna um cliente de teste para a aplicação Flask"""
    with test_app.test_client() as client:
        yield client

@pytest.fixture(scope="function")
def test_user(test_app: Flask) -> Generator[User, None, None]:
    """Fixture que cria um usuário de teste"""
    with test_app.app_context():
        test_user = User(
            username='testuser',
            email='testuser@example.com'
        )
        test_user.set_password('testpass')
        db.session.add(test_user)
        db.session.commit()
        logger.debug(f"Usuário de teste criado: {test_user.username}")
        yield test_user
        db.session.delete(test_user)
        db.session.commit()

@pytest.fixture(scope="function")
def test_task(test_app: Flask, test_user: User) -> Generator[Task, None, None]:
    """Fixture que cria uma tarefa de teste"""
    with test_app.app_context():
        task = Task(
            title='Test Task',
            description='Test description',
            user_id=test_user.id
        )
        db.session.add(task)
        db.session.commit()
        yield task
        db.session.delete(task)
        db.session.commit()

@pytest.fixture(scope="function")
def test_system_log(test_app: Flask, test_user: User) -> Generator[SystemLog, None, None]:
    """Fixture que cria um log de sistema de teste"""
    with test_app.app_context():
        log = SystemLog(
            action='Test action',
            user_id=test_user.id
        )
        db.session.add(log)
        db.session.commit()
        yield log
        db.session.delete(log)
        db.session.commit()

@pytest.fixture(scope="module")
def live_server(test_app: Flask) -> Generator[str, None, None]:
    """Fixture que inicia o servidor Flask em modo de teste"""
    # Configurar o servidor para rodar em modo de teste
    test_app.config['TESTING'] = True
    test_app.config['LIVESERVER_PORT'] = 5000
    test_app.config['LIVESERVER_TIMEOUT'] = 10
    
    # Iniciar o servidor em uma thread separada
    server = threading.Thread(target=test_app.run, kwargs={
        'host': 'localhost',
        'port': 5000,
        'debug': False,
        'use_reloader': False,
        'threaded': True
    })
    
    server.daemon = True
    server.start()
    
    # Aguardar o servidor iniciar
    time.sleep(5)  # Aumentei o tempo de espera para garantir que o servidor esteja pronto
    
    # Verificar se o servidor está respondendo
    import requests
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.fail("Server failed to start")
    
    yield 'http://localhost:5000'
    
    # Parar o servidor
    test_app.do_teardown_appcontext()
    server.join(timeout=5)