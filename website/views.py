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

@views.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    """
    Handle GET and POST requests for the feedback page.
    """
    if request.method == "POST":
        # Get the user ID from the request data
        feedback = json.loads(request.data)
        print(feedback)

    return render_template("feedback.html", user=current_user)

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

@views.route("/delete-sessions", methods=["POST"])
def delete_sessions():
    """
    Handle POST request for deleting all training sessions.
    """
    # Get the user ID from the request data
    user = json.loads(request.data)
    userID = user["user"]

    # Find the user in the database
    user = User.query.get(userID)

    # Check if the user exists and if it's the current user
    if user and user.id == current_user.id:
        # Delete all training sessions from the database
        for session in db.session.query(TrainingSession).filter_by(user_id=user.id):
            for blockofblocks in db.session.query(BlockOfBlocks).filter_by(session_id=session.id):
                for block in db.session.query(Block).filter_by(blockofblocks_id=blockofblocks.id):
                    db.session.delete(block)
                db.session.delete(blockofblocks)
            db.session.delete(session)

        db.session.commit()

    # Redirect to the home page
    return redirect(url_for("training.view_sessions"))
