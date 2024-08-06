from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, TrainingSession
from . import db
import json

views = Blueprint("views", __name__)


# Route for the home page
@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    """
    Handle GET and POST requests for the home page.
    """
    # Check if the user has any training sessions
    sessions = False if not TrainingSession.query.filter_by(user_id=current_user.id).all() else True
    return render_template("home.html", user=current_user, sessions=sessions)


# Route for the settings page
@views.route("/settings", methods=["GET", "POST"])
def settings():
    """
    Handle GET and POST requests for the settings page.
    """
    return render_template("settings.html", user=current_user, userID=current_user.id)


# Route for deleting an account
@views.route("/delete-account", methods=["POST"])
def delete_account():
    """
    Handle POST request for deleting an account.
    """
    # Get the user ID from the request data
    user = json.loads(request.data)
    userID = user["user"]

    # Find the user in the database
    user = User.query.get(userID)

    # Check if the user exists and if it's the current user
    if user and user.id == current_user.id:
        # Delete the user from the database
        db.session.delete(user)
        db.session.commit()

    # Redirect to the login page
    return redirect(url_for("auth.login"))

