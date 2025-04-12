"""Arquivo centralizado para definir uma u00fanica instu00e2ncia do SQLAlchemy.

Este arquivo define a instu00e2ncia singleton do SQLAlchemy que deve ser usada em todo o projeto.
"""
from flask_sqlalchemy import SQLAlchemy

# Instu00e2ncia u00fanica (singleton) do SQLAlchemy
db = SQLAlchemy()
