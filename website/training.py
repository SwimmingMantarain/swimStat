from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import User, TrainingSession, BlockOfBlocks, Block
from .views import views
from . import db
import json

training = Blueprint("training", __name__)

@training.route("/add-session", methods=["POST", "GET"])
@login_required
def add_session():
    if request.method == "POST":
        data = request.get_json()
        if data:
            session_name = data["sessionName"]
            sections = {}
            section_count = 0
            contains_set = False
            for section_id in data["section-ids"]:
                block_count = int(data[f"section[{section_id.replace('section-', '')}][blockCount]"])
                section_name = data[f"{section_id}[name]"]
                try:
                    section_is_set = True if data[f"{section_id}[isSet]"] == "true" else False
                    if section_is_set:
                        contains_set = True
                except KeyError:
                    section_is_set = False
                blocks = {}

                if block_count > 0:
                    for i in range(block_count):
                        block_id = f"block-{i + 1}"
                        distance = data[f"{section_id}[{block_id}][distance]"]
                        repeat_count = data[f"{section_id}[{block_id}][repeat]"]
                        stroke = data[f"{section_id}[{block_id}][strokes]"]
                        exercise = data[f"{section_id}[{block_id}][exercise]"]

                        blocks[block_id] = {
                            "distance": distance,
                            "repeatCount": repeat_count,
                            "stroke": stroke,
                            "exercise": exercise
                        }

                sections[section_id] = {"name": section_name, "blockCount": block_count, "blocks": blocks, "isSet": section_is_set}
                section_count += 1

            user = User.query.get(current_user.id)
            session = TrainingSession(name=session_name, user_id=current_user.id, contains_set=contains_set)
            total_distance = 0

            for i in range(section_count):
                section_id = f"section-{i + 1}"
                section_name = sections[section_id]["name"]
                section_is_set = sections[section_id]["isSet"]
                block_count = sections[section_id]["blockCount"]
                blocks = sections[section_id]["blocks"]
                section_blocks = BlockOfBlocks(name=section_name, training_session=session, is_set=section_is_set)

                for x in range(block_count):
                    block_id = f"block-{x + 1}"
                    block_data = blocks[block_id]
                    block = Block(
                        distance=block_data["distance"],
                        repeatCount=block_data["repeatCount"],
                        stroke=block_data["stroke"],
                        exercise=block_data["exercise"],
                        block_of_blocks=section_blocks
                    )

                    total_distance += int(block_data["distance"]) * int(block_data["repeatCount"])
                    db.session.add(block)
                session.blocks.append(section_blocks)


            session.total_distance = total_distance
            user.training_sessions.append(session)
            db.session.commit()

            return jsonify({"redirect": url_for("training.view_sessions")})

    return render_template("add_session.html", user=current_user, userID=current_user.id)

@training.route("/edit-session")
@login_required
def edit_session():
    return render_template("edit_session.html", user=current_user)

@training.route("/delete-session", methods=["POST"])
@login_required
def delete_session():
    if request.method == "POST":
        data = request.get_json()
        if data:
            sessionID = data["sessionID"]
            session = TrainingSession.query.get(sessionID)
            if session:
                db.session.delete(session)
                db.session.commit()
                return jsonify({"redirect": url_for("training.view_sessions")})

@training.route("/view_sessions")
@login_required
def view_sessions():
    return render_template("view_sessions.html", user=current_user, sessions=current_user.training_sessions)