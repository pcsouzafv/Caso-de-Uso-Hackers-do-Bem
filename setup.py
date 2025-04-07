"""
Configuração do pacote Task Manager
"""
from setuptools import setup, find_packages

setup(
    name="task-manager",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==2.0.1",
        "Flask-SQLAlchemy==2.5.1",
        "SQLAlchemy==1.4.54",
        "Werkzeug==2.0.1",
        "pytest==7.4.0",
        "pytest-flask==1.3.0",
        "selenium==4.31.0"
    ],
    python_requires=">=3.8",
    zip_safe=False
)
