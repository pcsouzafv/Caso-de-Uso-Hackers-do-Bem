# Re-export dos modelos do models_manager
# Este arquivo é mantido para compatibilidade com código existente

from models_manager import MainUser as User
from models_manager import MainTask as Task
from models_manager import MainSystemLog as SystemLog

# Re-export das funções auxiliares
from models_manager import setup_test_db, cleanup_test_db

# Note: as classes originais (OldUser, OldTask, OldSystemLog) são mantidas abaixo
# apenas para compatibilidade com código legado que possa depender delas

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import Base, db

# Modelos para a API FastAPI
class OldUser(Base):
    """Modelo antigo de usuário para API FastAPI.
    Mantido por compatibilidade com código legado.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    updated_at = Column(DateTime(timezone=True), onupdate=text("NOW()"))
    
    tasks = relationship("OldTask", back_populates="owner")
    logs = relationship("OldSystemLog", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class OldTask(Base):
    """Modelo antigo de tarefa para API FastAPI.
    Mantido por compatibilidade com código legado.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    updated_at = Column(DateTime(timezone=True), onupdate=text("NOW()"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("OldUser", back_populates="tasks")

    def __repr__(self):
        return f"<Task {self.title}>"

class OldSystemLog(Base):
    """Modelo antigo de log do sistema para API FastAPI.
    Mantido por compatibilidade com código legado.
    """
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(255), nullable=False)
    details = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=text("NOW()"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("OldUser", back_populates="logs")

    def __repr__(self):
        return f"<SystemLog {self.action}>"
