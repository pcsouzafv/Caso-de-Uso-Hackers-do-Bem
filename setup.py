"""
Configuração do pacote Task Manager

Este arquivo define as configurações de empacotamento para o projeto Task Manager,
incluindo dependências e metadados.
"""
from setuptools import setup, find_packages

setup(
    name="task-manager",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'task_manager': ['py.typed'],
    },
    zip_safe=False,
    install_requires=[
        'Flask==2.0.1',
        'Flask-SQLAlchemy==2.5.1',
        'Flask-Login==0.6.3',
        'Werkzeug==2.0.1',
        'Jinja2==3.1.6',
        'SQLAlchemy==1.4.23',
        'Flask-Migrate==3.1.0',
        'email-validator==1.1.3',
        'gunicorn==20.1.0',
        'python-dotenv==0.19.0',
    ],
)
