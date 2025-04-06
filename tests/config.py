# tests/config.py
import os

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