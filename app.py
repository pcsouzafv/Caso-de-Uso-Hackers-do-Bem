from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.completed)
    pending_tasks = total_tasks - completed_tasks
    
    return render_template('index.html', 
                         tasks=tasks,
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         pending_tasks=pending_tasks)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            log = SystemLog(action=f'User {username} logged in', user_id=user.id)
            db.session.add(log)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    log = SystemLog(action=f'User {current_user.username} logged out', user_id=current_user.id)
    db.session.add(log)
    db.session.commit()
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))
            
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
            
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    users = User.query.all()
    tasks = Task.query.all()
    logs = SystemLog.query.order_by(SystemLog.timestamp.desc()).limit(50).all()
    return render_template('admin_dashboard.html', users=users, tasks=tasks, logs=logs)

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    due_date_str = request.form.get('due_date')
    
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d') if due_date_str else None
    except ValueError:
        due_date = None
    
    task = Task(
        title=title,
        description=description,
        user_id=current_user.id
    )
    
    db.session.add(task)
    log = SystemLog(action=f'Tarefa "{title}" criada', user_id=current_user.id)
    db.session.add(log)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/task/<int:id>/toggle')
@login_required
def toggle_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id or current_user.is_admin:
        task.completed = not task.completed
        action = 'concluída' if task.completed else 'marcada como pendente'
        log = SystemLog(action=f'Tarefa "{task.title}" {action}', user_id=current_user.id)
        db.session.add(log)
        db.session.commit()
    return redirect(request.referrer or url_for('user_dashboard'))

@app.route('/task/<int:id>/delete')
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id == current_user.id or current_user.is_admin:
        log = SystemLog(action=f'Tarefa "{task.title}" excluída', user_id=current_user.id)
        db.session.add(log)
        db.session.delete(task)
        db.session.commit()
    return redirect(request.referrer or url_for('user_dashboard'))

@app.route('/admin/user/add', methods=['POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == 'on'
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists')
        return redirect(url_for('admin_dashboard'))
    
    user = User(
        username=username,
        is_admin=is_admin
    )
    user.set_password(password)
    
    db.session.add(user)
    log = SystemLog(action=f'User {username} created', user_id=current_user.id)
    db.session.add(log)
    db.session.commit()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/user/delete/<user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        abort(403)
    
    user = User.query.get_or_404(id)
    log = SystemLog(action=f'Usuário {user.username} excluído', user_id=current_user.id)
    db.session.add(log)
    db.session.delete(user)
    log = SystemLog(action=f'Usuário {user.username} foi deletado por {current_user.username}', user_id=current_user.id)
    db.session.add(log)
    db.session.commit()
    
    return redirect(url_for('admin_dashboard'))

def create_admin():
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                is_admin=True
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    create_admin()
    app.run(host='0.0.0.0', port=8080, debug=True)
