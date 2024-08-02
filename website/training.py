from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User
from . import db
import json

training = Blueprint("training", __name__)

@training.route("/add-session", methods=["POST", "GET"])
@login_required
def add_session():
    if request.method == "POST":
        json_data = request.get_json()
        if json_data:
            print(json_data)
            sessionName = json_data["sessionName"]
            sections = {}
            sectionCount = 0
            for section in json_data["section-ids"]:
                blockCount = int(json_data[f"section[{section.replace('section-', '')}][blockCount]"])
                name = json_data[f"{section}[name]"]
                blocks = {}

                if blockCount > 0:
                    for i in range(blockCount):
                        block = f"block-{i + 1}"
                        distance = json_data[f"{section}[{block}][distance]"]
                        repeatCount = json_data[f"{section}[{block}][repeat]"]
                        stroke = json_data[f"{section}[{block}][strokes]"]
                        exercise = json_data[f"{section}[{block}][exercise]"]
                        blocks[block] = {"distance": distance, "repeatCount": repeatCount, "stroke": stroke, "exercise": exercise}

                sections[section] = {"name": name, "blockCount": blockCount, "blocks": blocks}
                sectionCount += 1
    
    return render_template("add_session.html", user=current_user)

@training.route("/edit-session")
@login_required
def edit_session():
    return render_template("edit_session.html", user=current_user)

@training.route("/delete-session")
@login_required
def delete_session():
    return render_template("delete_session.html", user=current_user)