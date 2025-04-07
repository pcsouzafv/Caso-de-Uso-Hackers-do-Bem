import os
from app.config import Config

# Configurações para testes

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configurações para testes funcionais com Selenium
class SeleniumConfig:
    CHROME_OPTIONS = {
        'binary_location': os.environ.get('CHROME_BIN', None),
        'arguments': [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--window-size=1920,1080'
        ]
    }
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 15
