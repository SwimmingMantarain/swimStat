from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
import json

training = Blueprint("training", __name__)

@training.route("/add-session")
@login_required
def add_session():
    return render_template("add_session.html", user=current_user)

@training.route("/edit-session")
@login_required
def edit_session():
    return render_template("edit_session.html", user=current_user)

@training.route("/delete-session")
@login_required
def delete_session():
    return render_template("delete_session.html", user=current_user)