from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, abort
from flask_login import login_required, current_user
from datetime import datetime
from ..models import Task, SystemLog
from .. import db

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/")
@login_required
def index():
    if current_user.is_admin:
        return redirect(url_for("admin.dashboard"))

    tasks = (
        Task.query.filter_by(user_id=current_user.id)
        .order_by(Task.created_at.desc())
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

@tasks_bp.route("/add", methods=["POST"])
@login_required
def add_task():
    title = request.form.get("title")
    description = request.form.get("description")
    due_date_str = request.form.get("due_date")

    if not title:
        flash("O tu00edtulo u00e9 obrigatu00f3rio")
        return redirect(url_for("tasks.index"))

    task = Task(title=title, description=description, user_id=current_user.id)

    if due_date_str:
        try:
            task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            flash("Data invu00e1lida")
            return redirect(url_for("tasks.index"))

    db.session.add(task)
    log = SystemLog(
        action=f"Tarefa '{title}' criada por {current_user.username}",
        user_id=current_user.id,
    )
    db.session.add(log)
    db.session.commit()

    return redirect(url_for("tasks.index"))

@tasks_bp.route("/toggle/<int:task_id>", methods=["POST"])
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    task.completed = not task.completed
    db.session.commit()

    log = SystemLog(
        action=f'Tarefa "{task.title}" {"concluu00edda" if task.completed else "reaberta"} por {current_user.username}',
        user_id=current_user.id,
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({"success": True})

@tasks_bp.route("/delete/<int:task_id>", methods=["DELETE"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    log = SystemLog(
        action=f'Tarefa "{task.title}" excluu00edda por {current_user.username}',
        user_id=current_user.id,
    )
    db.session.add(log)
    db.session.delete(task)
    db.session.commit()

    return jsonify({"success": True})
