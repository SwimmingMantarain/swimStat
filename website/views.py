from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
import json

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/account", methods=["GET", "POST"])
@login_required
def account():
    return render_template("account.html", user=current_user)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note deleted", category="success")
    return jsonify({})

@views.route("/delete-account", methods=["POST", "GET"])
@login_required
def delete_account():
    user = json.loads(request.data)
    userID = user["userId"]
    user = User.query.get(userID)
    if user:
        if user.id == current_user.id:
            db.session.delete(user)
            db.session.commit()
            flash("Account deleted", category="success")

    return redirect(url_for('auth.login'))
