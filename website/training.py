from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import User, TrainingSession, BlockOfBlocks, Block
from .views import views
from . import db

training = Blueprint("training", __name__)

@training.route("/add-session", methods=["POST", "GET"])
@login_required
def add_session():
    """
    Handle POST and GET requests for adding a training session.
    """
    if request.method == "POST":
        data = request.get_json()
        if data:
            # Extract session name and sections from POST data
            session_name = data["sessionName"]
            sections = {}
            contains_set = False

            try:
                section_ids = data["section-ids"]
                if not section_ids:
                    flash("Please add at least one section", category="error")
                    return jsonify({}), 400
            except KeyError:
                flash("Please add at least one section", category="error")
                return jsonify({}), 400
            
            if len(section_ids) == 9:
                section_ids = [f"{section_ids}"]

            # Process each section and its blocks
            for section_id in section_ids:
                section_id = f"{section_id.replace('section-', '')}"
                block_count = int(data[f"section[{section_id}][blockCount]"])

                if block_count < 0:
                    flash("Please add at least one block", category="error")
                    return jsonify({}), 400

                section_name = data[f"section-{section_id}[name]"]

                try:
                    is_set = True if data[f"section-{section_id}[isSet]"] == "true" else False
                    if is_set:
                        contains_set = True
                except KeyError:
                    is_set = False

                blocks = {}
                if block_count > 0:
                    for i in range(1, block_count + 1):
                        block_id = f"block-{i}"
                        distance = data[f"section-{section_id}[{block_id}][distance]"]
                        repeat_count = data[f"section-{section_id}[{block_id}][repeat]"]
                        stroke = data[f"section-{section_id}[{block_id}][strokes]"]
                        exercise = data[f"section-{section_id}[{block_id}][exercise]"]
                        blocks[block_id] = {
                            "distance": distance,
                            "repeatCount": repeat_count,
                            "stroke": stroke,
                            "exercise": exercise
                        }

                sections[section_id] = {
                    "name": section_name,
                    "blockCount": block_count,
                    "blocks": blocks,
                    "isSet": is_set
                }

            user = User.query.get(current_user.id)
            session = TrainingSession(name=session_name, user_id=current_user.id, contains_set=contains_set)
            total_distance = 0
            set_distance = 0

            # Process each section's blocks and add them to the database
            for i, section_id in enumerate(sections, start=1):
                section_name = sections[section_id]["name"]
                is_set = sections[section_id]["isSet"]
                block_count = sections[section_id]["blockCount"]
                blocks = sections[section_id]["blocks"]

                section_blocks = BlockOfBlocks(name=section_name, training_session=session, is_set=is_set)

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

                    if is_set:
                        set_distance += int(block_data["distance"]) * int(block_data["repeatCount"])

                    db.session.add(block)

                session.blocks.append(section_blocks)

            session.total_distance = total_distance
            session.set_distance = set_distance
            user.training_sessions.append(session)
            db.session.commit()

            return jsonify({"redirect": url_for("training.view_sessions")})
        
    return render_template("add_session.html", user=current_user, userID=current_user.id)

@training.route("/edit-session/<sessionID>", methods=["GET", "POST"])
@login_required
def edit_session(sessionID):
    """
    Handle GET and POST requests for editing a training session.

    Args:
        sessionID (str): The ID of the training session to edit.

    Returns:
        If the request method is POST, this function returns a JSON response with a redirect URL.
        If the request method is GET, this function renders the edit_session.html template.
    """
    # Get the training session with the given ID
    session = TrainingSession.query.get(sessionID)

    if request.method == "POST":
        if session:
            # Delete the session, its associated blockofblocks and their associated blocks
            for blockofblocks in session.blocks:
                for block in blockofblocks.blocks:
                    db.session.delete(block)
                db.session.delete(blockofblocks)
            db.session.delete(session)
            db.session.commit()
        
        # Extract session name and sections from POST data
        data = request.get_json()

        # Check if data exists
        if data:
            session_name = data["sessionName"]
            sections = {}
            contains_set = False
            total_distance = 0
            set_distance = 0

            try:
                section_ids = data["section-ids"]
                # Check if at least one section is added
                if not section_ids:
                    flash("Please add at least one section", category="error")
                    return jsonify({}), 400
            except KeyError:
                flash("Please add at least one section", category="error")
                return jsonify({}), 400
            
            # If only one section is added, convert it to a list
            if len(section_ids) == 9:
                section_ids = [f"{section_ids}"]

            # Process each section and its blocks
            for section_id in section_ids:
                section_id = f"{section_id.replace('section-', '')}"
                block_count = int(data[f"section[{section_id}][blockCount]"])

                # Check if at least one block is added
                if block_count < 0:
                    flash("Please add at least one block", category="error")
                    return jsonify({}), 400

                section_name = data[f"section-{section_id}[name]"]

                try:
                    is_set = True if data[f"section-{section_id}[isSet]"] == "true" else False
                    if is_set:
                        contains_set = True
                except KeyError:
                    is_set = False

                blocks = {}
                if block_count > 0:
                    for i in range(1, block_count + 1):
                        block_id = f"block-{i}"
                        distance = data[f"section-{section_id}[{block_id}][distance]"]
                        repeat_count = data[f"section-{section_id}[{block_id}][repeat]"]
                        stroke = data[f"section-{section_id}[{block_id}][strokes]"]
                        exercise = data[f"section-{section_id}[{block_id}][exercise]"]
                        blocks[block_id] = {
                            "distance": distance,
                            "repeatCount": repeat_count,
                            "stroke": stroke,
                            "exercise": exercise
                        }

                        total_distance += int(distance) * int(repeat_count)

                        if is_set:
                            set_distance += int(distance) * int(repeat_count)

                sections[section_id] = {
                    "name": section_name,
                    "blockCount": block_count,
                    "blocks": blocks,
                    "isSet": is_set
                }

            # Create a new training session
            session = TrainingSession(name=session_name, user_id=current_user.id)
            db.session.add(session)

            # Process each section's blocks and update the database
            for i, section_id in enumerate(sections, start=1):
                section_name = sections[section_id]["name"]
                is_set = sections[section_id]["isSet"]
                block_count = sections[section_id]["blockCount"]
                blocks = sections[section_id]["blocks"]

                # Create a new block of blocks
                section_blocks = BlockOfBlocks(name=section_name, training_session=session, is_set=is_set)
                session.blocks.append(section_blocks)

                # Create each block
                for x in range(block_count):
                    block_id = f"block-{x + 1}"
                    block_data = blocks[block_id]

                    block = Block(
                        distance=block_data["distance"],
                        repeatCount=block_data["repeatCount"],
                        stroke=block_data["stroke"],
                        exercise=block_data["exercise"],
                        block_of_blocks_id=section_blocks.id
                    )

                    section_blocks.blocks.append(block)

            # Update the session details
            session.name = session_name
            session.total_distance = total_distance
            session.set_distance = set_distance
            session.contains_set = contains_set
            db.session.commit()

            # Redirect to the view_sessions page
            return jsonify({"redirect": url_for("training.view_sessions")})

    # Convert the session to json so jinja and js stop complaining
    session = session.to_dict()
    return render_template("edit_session.html", user=current_user, session=session, sessionID=sessionID)

@training.route("/delete-session", methods=["POST"])
@login_required
def delete_session():
    """
    Handle POST requests for deleting a training session.
    """
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
    """
    Handle GET requests for viewing training sessions.
    """
    return render_template("view_sessions.html", user=current_user, sessions=current_user.training_sessions)

@training.route("/submit-session", methods=["GET", "POST"])
@login_required
def submit_session():
    """
    Handle GET and POST requests for submitting a training session.
    """
    return render_template("submit_session.html", user=current_user, sessions=current_user.training_sessions)
