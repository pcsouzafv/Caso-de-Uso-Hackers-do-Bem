from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

import models
from database import SessionLocal, engine, Base
from schemas import TaskCreate, TaskUpdate, UserCreate, UserUpdate, Task, User, SystemLog, SystemLogCreate

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API", description="API para gerenciamento de tarefas")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Dependência para obter sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rotas para a interface web
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# API endpoints para tarefas
@app.post("/api/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        due_date=task.due_date,
        owner_id=1  # ID padrão para teste
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Criar log de atividade
    log = models.SystemLog(
        action=f"Tarefa '{task.title}' criada",
        details=f"Nova tarefa adicionada ao sistema",
        user_id=1  # Usuário padrão para API
    )
    db.add(log)
    db.commit()
    
    return db_task

@app.get("/api/tasks/", response_model=List[Task])
async def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).offset(skip).limit(limit).all()
    return tasks

@app.get("/api/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return db_task

@app.put("/api/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    # Atualiza apenas os campos fornecidos
    update_data = task.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    
    # Criar log de atividade
    log = models.SystemLog(
        action=f"Tarefa '{db_task.title}' atualizada",
        details=f"Campos atualizados: {', '.join(update_data.keys())}",
        user_id=1  # Usuário padrão para API
    )
    db.add(log)
    db.commit()
    
    return db_task

@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    task_title = db_task.title
    db.delete(db_task)
    
    # Criar log de atividade
    log = models.SystemLog(
        action=f"Tarefa '{task_title}' excluída",
        details=f"Tarefa removida permanentemente do sistema",
        user_id=1  # Usuário padrão para API
    )
    db.add(log)
    db.commit()
    
    return None

# API endpoints para usuários
@app.post("/api/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verifica se o usuário já existe
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já registrado")
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    # Cria novo usuário
    new_user = models.User(
        username=user.username,
        email=user.email,
        is_admin=user.is_admin,
        is_active=user.is_active
    )
    new_user.set_password(user.password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Criar log de atividade
    log = models.SystemLog(
        action=f"Usuário '{user.username}' criado",
        details=f"Novo usuário registrado no sistema",
        user_id=new_user.id
    )
    db.add(log)
    db.commit()
    
    return new_user

@app.get("/api/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.get("/api/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user

@app.put("/api/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Atualiza apenas os campos fornecidos
    update_data = user.dict(exclude_unset=True)
    
    # Trata a senha separadamente
    if "password" in update_data:
        db_user.set_password(update_data["password"])
        del update_data["password"]
    
    # Atualiza os demais campos
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    
    # Criar log de atividade
    log = models.SystemLog(
        action=f"Usuário '{db_user.username}' atualizado",
        details=f"Campos atualizados: {', '.join(update_data.keys())}",
        user_id=db_user.id
    )
    db.add(log)
    db.commit()
    
    return db_user

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    username = db_user.username
    db.delete(db_user)
    
    # Criar log de atividade (usando o ID 1 como administrador)
    log = models.SystemLog(
        action=f"Usuário '{username}' removido",
        details=f"Usuário excluído permanentemente do sistema",
        user_id=1  # ID do administrador
    )
    db.add(log)
    db.commit()
    
    return None

# Logs do sistema
@app.get("/api/logs/", response_model=List[SystemLog])
async def read_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = db.query(models.SystemLog).order_by(models.SystemLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
