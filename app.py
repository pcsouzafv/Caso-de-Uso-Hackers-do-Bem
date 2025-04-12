import os
from datetime import datetime
from pathlib import Path

from flask import (Flask, abort, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from werkzeug.security import check_password_hash, generate_password_hash

from db import db

# Importar os modelos do gerenciador centralizado
from models_manager import MainUser, MainTask, MainSystemLog

# Inicialização do LoginManager
login_manager = LoginManager()

# Função factory que cria e configura a aplicação Flask
def create_app(config=None):
    """Factory que cria e configura a aplicação Flask"""
    app_instance = Flask(__name__)
    app_instance.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')
    app_instance.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskmanager.db"
    app_instance.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Se estiver em modo de teste, sobreescrevemos a configuração
    if config == 'testing':
        app_instance.config["TESTING"] = True
        app_instance.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app_instance.config["WTF_CSRF_ENABLED"] = False
    
    db.init_app(app_instance)
    login_manager.init_app(app_instance)
    login_manager.login_view = "login"
    
    return app_instance

# Criação do app
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    return MainUser.query.get(int(user_id))

@app.route("/")
@login_required
def index():
    if current_user.is_admin:
        return redirect(url_for("admin_dashboard"))

    tasks = (
        MainTask.query.filter_by(user_id=current_user.id)
        .order_by(MainTask.created_at.desc())
        .all()
    )

    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.completed)
    pending_tasks = total_tasks - completed_tasks

    return render_template(
        "index.html",
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
        
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = MainUser.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            log = MainSystemLog(action=f"Usuário {username} fez login", user_id=user.id)
            db.session.add(log)
            db.session.commit()
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha inválidos")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    log = MainSystemLog(
        action=f"Usuário {current_user.username} fez logout", user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
        
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            flash('Senhas não coincidem', 'error')
            return redirect(url_for('register'))
            
        if MainUser.query.filter_by(username=username).first():
            flash('Nome de usuário já existe', 'error')
            return redirect(url_for('register'))
            
        if MainUser.query.filter_by(email=email).first():
            flash('Email já cadastrado', 'error')
            return redirect(url_for('register'))
            
        user = MainUser(
            username=username,
            email=email,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template('register.html')


@app.route("/admin")
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    users = MainUser.query.all()
    tasks = MainTask.query.all()
    logs = MainSystemLog.query.order_by(MainSystemLog.timestamp.desc()).limit(50).all()

    return render_template("admin_dashboard.html", users=users, tasks=tasks, logs=logs)


@app.route("/add_task", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title")
    description = request.form.get("description")
    due_date_str = request.form.get("due_date")

    if not title:
        flash("O título é obrigatório")
        return redirect(url_for("index"))

    task = MainTask(title=title, description=description, user_id=current_user.id)

    if due_date_str:
        try:
            task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Data inválida")
            return redirect(url_for("index"))

    db.session.add(task)
    log = MainSystemLog(
        action=f"Tarefa '{title}' criada por {current_user.username}",
        user_id=current_user.id,
        details="Nova tarefa adicionada"
    )
    db.session.add(log)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/toggle_task/<int:task_id>", methods=["POST"])
@login_required
def toggle_task(task_id):
    task = MainTask.query.get_or_404(task_id)
    if task.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    task.completed = not task.completed
    db.session.commit()

    log = MainSystemLog(
        action=f'Tarefa "{task.title}" {"concluída" if task.completed else "reaberta"} por {current_user.username}',
        user_id=current_user.id,
        details=f"Status da tarefa alterado para {task.completed}"
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/delete_task/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = MainTask.query.get_or_404(task_id)
    if task.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    log = MainSystemLog(
        action=f'Tarefa "{task.title}" excluída por {current_user.username}',
        user_id=current_user.id,
        details="Tarefa removida permanentemente"
    )
    db.session.add(log)
    db.session.delete(task)
    db.session.commit()

    return jsonify({"success": True})


@app.route("/admin/user/add", methods=["POST"])
@login_required
def add_user():
    if not current_user.is_admin:
        return redirect(url_for("index"))

    username = request.form.get("username")
    email = request.form.get("email", f"{username}@example.com")
    password = request.form.get("password")
    is_admin = request.form.get("is_admin") == "on"

    if MainUser.query.filter_by(username=username).first():
        flash("Nome de usuário já existe")
        return redirect(url_for("admin_dashboard"))

    user = MainUser(username=username, email=email, is_admin=is_admin)
    user.set_password(password)

    db.session.add(user)
    log = MainSystemLog(action=f"Usuário {username} criado", user_id=current_user.id)
    db.session.add(log)
    db.session.commit()

    return redirect(url_for("admin_dashboard"))


@app.route("/user/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        abort(403)

    user = MainUser.query.get_or_404(user_id)
    if user.id == current_user.id:
        abort(400)  # Não pode deletar a si mesmo

    db.session.delete(user)
    log = MainSystemLog(
        action=f"Usuário {user.username} foi deletado por {current_user.username}",
        user_id=current_user.id,
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"success": True})


if __name__ == "__main__":
    with app.app_context():
        # Inicializar o banco de dados
        db.create_all()
        
        # Criar usuário admin se não existir
        admin_user = MainUser.query.filter_by(username="admin").first()
        if not admin_user:
            admin_user = MainUser(
                username="admin",
                email="admin@example.com",
                is_admin=True
            )
            admin_user.set_password("admin")
            db.session.add(admin_user)
            db.session.commit()
            
            # Criar log
            log = MainSystemLog(
                action="Admin user created",
                details="Initial admin user created during app initialization",
                user_id=admin_user.id
            )
            db.session.add(log)
            db.session.commit()
    
    app.run(host="0.0.0.0", port=8080, debug=True)
