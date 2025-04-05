from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            log = SystemLog(action=f'Usuário {username} fez login', user_id=user.id)
            db.session.add(log)
            db.session.commit()
            return redirect(url_for('index'))
        
        flash('Usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    log = SystemLog(action=f'Usuário {current_user.username} fez logout', user_id=current_user.id)
    db.session.add(log)
    db.session.commit()
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('user_dashboard'))
    users = User.query.all()
    tasks = Task.query.all()
    logs = SystemLog.query.order_by(SystemLog.timestamp.desc()).limit(50).all()
    return render_template('admin_dashboard.html', users=users, tasks=tasks, logs=logs)

@app.route('/dashboard')
@login_required
def user_dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return render_template('user_dashboard.html', tasks=tasks)

@app.route('/task/add', methods=['POST'])
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
        due_date=due_date,
        user_id=current_user.id
    )
    
    db.session.add(task)
    log = SystemLog(action=f'Tarefa "{title}" criada', user_id=current_user.id)
    db.session.add(log)
    db.session.commit()
    
    return redirect(url_for('user_dashboard'))

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
        return redirect(url_for('user_dashboard'))
    
    username = request.form.get('username')
    password = request.form.get('password')
    is_admin = request.form.get('is_admin') == 'on'
    
    if User.query.filter_by(username=username).first():
        flash('Nome de usuário já existe')
        return redirect(url_for('admin_dashboard'))
    
    user = User(
        username=username,
        is_admin=is_admin
    )
    user.set_password(password)
    
    db.session.add(user)
    log = SystemLog(action=f'Usuário {username} criado', user_id=current_user.id)
    db.session.add(log)
    db.session.commit()
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/user/<int:id>/delete')
@login_required
def delete_user(id):
    if not current_user.is_admin or id == current_user.id:
        return redirect(url_for('admin_dashboard'))
    
    user = User.query.get_or_404(id)
    log = SystemLog(action=f'Usuário {user.username} excluído', user_id=current_user.id)
    db.session.add(log)
    db.session.delete(user)
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
