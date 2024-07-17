from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
import json

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route("/settings", methods=["GET", "POST"])
def settings():
    return render_template("settings.html", user=current_user, userID=current_user.id)

@views.route("/delete-account", methods=["POST", "GET"])
def delete_account():
    user = json.loads(request.data)
    userID = user["user"]
    user = User.query.get(userID)
    if user:
        if user.id == current_user.id:
            db.session.delete(user)
            db.session.commit()
    
    return redirect(url_for("auth.login"))
