from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import User, Task, SystemLog
from database import db

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(owner_id=current_user.id).all()
    return render_template('index.html', tasks=tasks)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso!')
            return redirect(url_for('main.index'))
        
        flash('Nome de usuário ou senha incorretos')
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso!')
    return redirect(url_for('main.login'))

@bp.route('/add_task', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    
    if not title:
        flash('O título é obrigatório')
        return redirect(url_for('main.index'))
    
    task = Task(
        title=title,
        description=description,
        due_date=datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None,
        owner_id=current_user.id
    )
    db.session.add(task)
    db.session.commit()
    
    # Criar log
    log = SystemLog(
        action=f'Tarefa "{title}" criada',
        details=f'Usuário {current_user.username} criou uma nova tarefa',
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()
    
    flash('Tarefa adicionada com sucesso!')
    return redirect(url_for('main.index'))

@bp.route('/complete_task/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.owner_id != current_user.id:
        flash('Você não tem permissão para completar esta tarefa')
        return redirect(url_for('main.index'))
    
    task.completed = True
    db.session.commit()
    
    # Criar log
    log = SystemLog(
        action=f'Tarefa "{task.title}" completada',
        details=f'Usuário {current_user.username} completou a tarefa',
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()
    
    flash('Tarefa completada com sucesso!')
    return redirect(url_for('main.index'))
