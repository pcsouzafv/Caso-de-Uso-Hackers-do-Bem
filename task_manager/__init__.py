"""Pacote Task Manager"""
from flask_sqlalchemy import SQLAlchemy

# Inicializa a extensão SQLAlchemy
db = SQLAlchemy()

# Importa os modelos e a aplicação depois para evitar circular imports
from .app import create_app
from .models import User, Task

__all__ = ["db", "User", "Task", "create_app"]
