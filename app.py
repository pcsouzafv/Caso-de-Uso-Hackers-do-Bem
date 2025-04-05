from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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
    
    if not title:
        flash('O título é obrigatório')
        return redirect(url_for('index'))
    
    task = Task(
        title=title,
        description=description,
        user_id=current_user.id
    )
    
    if due_date_str:
        try:
            task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Data inválida')
            return redirect(url_for('index'))
    
    db.session.add(task)
    log = SystemLog(action=f'Tarefa "{title}" criada por {current_user.username}', user_id=current_user.id)
    db.session.add(log)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/toggle_task/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    task.completed = not task.completed
    db.session.commit()
    
    log = SystemLog(
        action=f'Tarefa "{task.title}" {"concluída" if task.completed else "reaberta"} por {current_user.username}',
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    log = SystemLog(
        action=f'Tarefa "{task.title}" excluída por {current_user.username}',
        user_id=current_user.id
    )
    db.session.add(log)
    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/admin/user/add', methods=['POST'])
@login_required
def add_user():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    
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

@app.route('/user/delete/<user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        abort(403)
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        abort(400)  # Não pode deletar a si mesmo
    
    db.session.delete(user)
    log = SystemLog(action=f'Usuário {user.username} foi deletado por {current_user.username}', user_id=current_user.id)
    db.session.add(log)
    db.session.commit()
    
    return jsonify({'success': True})

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
