import os
import shutil
import datetime
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3
import zipfile
import json

class BackupManager:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.backup_dir = os.path.join(app.root_path, 'backups')
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup(self):
        """Cria um backup completo do banco de dados"""
        try:
            # Gera um nome único para o backup
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f'backup_{timestamp}.zip'
            backup_path = os.path.join(self.backup_dir, backup_name)

            # Cria um arquivo ZIP para o backup
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
                # Backup do banco de dados
                db_path = current_app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
                backup_zip.write(db_path, 'task_manager.db')

                # Backup das configurações
                config = {
                    'timestamp': timestamp,
                    'version': '1.0'
                }
                backup_zip.writestr('backup_config.json', json.dumps(config))

            return backup_path

        except Exception as e:
            raise Exception(f'Erro ao criar backup: {str(e)}')

    def restore_backup(self, backup_path):
        """Restaura um backup do banco de dados"""
        try:
            # Verifica se o arquivo existe
            if not os.path.exists(backup_path):
                raise FileNotFoundError('Backup não encontrado')

            # Extrai o backup
            with zipfile.ZipFile(backup_path, 'r') as backup_zip:
                # Restaura o banco de dados
                db_path = current_app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
                backup_zip.extract('task_manager.db', path=os.path.dirname(db_path))
                
                # Move o arquivo restaurado para o local correto
                shutil.move(
                    os.path.join(os.path.dirname(db_path), 'task_manager.db'),
                    db_path
                )

            return True

        except Exception as e:
            raise Exception(f'Erro ao restaurar backup: {str(e)}')

    def list_backups(self):
        """Lista todos os backups disponíveis"""
        try:
            backups = []
            for filename in os.listdir(self.backup_dir):
                if filename.endswith('.zip'):
                    backup_path = os.path.join(self.backup_dir, filename)
                    timestamp = filename.replace('backup_', '').replace('.zip', '')
                    size = os.path.getsize(backup_path)
                    backups.append({
                        'filename': filename,
                        'timestamp': timestamp,
                        'size': size,
                        'path': backup_path
                    })
            return sorted(backups, key=lambda x: x['timestamp'], reverse=True)

        except Exception as e:
            raise Exception(f'Erro ao listar backups: {str(e)}')

    def delete_backup(self, backup_path):
        """Remove um backup específico"""
        try:
            if os.path.exists(backup_path):
                os.remove(backup_path)
            return True

        except Exception as e:
            raise Exception(f'Erro ao deletar backup: {str(e)}')

    def get_latest_backup(self):
        """Retorna o último backup disponível"""
        backups = self.list_backups()
        if backups:
            return backups[0]
        return None
