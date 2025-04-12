from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, abort
from flask_login import login_required, current_user
from ..models import User, Task, SystemLog
from .. import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route("/")
@login_required
def dashboard():
    if not current_user.is_admin:
        return redirect(url_for("tasks.index"))

    users = User.query.all()
    tasks = Task.query.all()
    logs = SystemLog.query.order_by(SystemLog.timestamp.desc()).limit(50).all()

    return render_template("admin_dashboard.html", users=users, tasks=tasks, logs=logs)

@admin_bp.route("/user/add", methods=["POST"])
@login_required
def add_user():
    if not current_user.is_admin:
        return redirect(url_for("tasks.index"))

    username = request.form.get("username")
    email = request.form.get("email", "")
    password = request.form.get("password")
    is_admin = request.form.get("is_admin") == "on"

    if User.query.filter_by(username=username).first():
        flash("Nome de usuário já existe")
        return redirect(url_for("admin.dashboard"))

    user = User(username=username, email=email, is_admin=is_admin)
    user.set_password(password)

    db.session.add(user)
    log = SystemLog(action=f"Usuário {username} criado", user_id=current_user.id)
    db.session.add(log)
    db.session.commit()

    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/user/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        abort(403)

    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        abort(400)  # Não pode deletar a si mesmo

    db.session.delete(user)
    log = SystemLog(
        action=f"Usuário {user.username} foi deletado por {current_user.username}",
        user_id=current_user.id,
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"success": True})
