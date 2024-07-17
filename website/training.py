from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
import json

training = Blueprint("training", __name__)

@training.route("/add-session")
@login_required
def add_session():
    return "<h1>Add Session</h1>"

@training.route("/edit-session")
@login_required
def edit_session():
    return "<h1>Edit Session</h1>"

@training.route("/delete-session")
@login_required
def delete_session():
    return "<h1>Delete Session</h1>"