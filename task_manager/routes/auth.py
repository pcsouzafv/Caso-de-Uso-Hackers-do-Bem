from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, SystemLog
from .. import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            log = SystemLog(action=f"Usuário {username} fez login", user_id=user.id)
            db.session.add(log)
            db.session.commit()
            return redirect(url_for("tasks.index"))
        else:
            flash("Usuário ou senha inválidos")
    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    log = SystemLog(
        action=f"Usuário {current_user.username} fez logout", user_id=current_user.id
    )
    db.session.add(log)
    db.session.commit()
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            flash('As senhas não coincidem', 'error')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe', 'error')
            return redirect(url_for('auth.register'))
            
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('tasks.index'))
    
    return render_template('register.html')
