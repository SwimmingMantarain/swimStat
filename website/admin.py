from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import User
from . import db
import subprocess
import re
import smtplib
from email.mime.text import MIMEText

admin = Blueprint("admin", __name__)

def create_admin():
    """
    Create an admin user.
    """
    user = User(
        email="admin@aquametrics.org",
        firstName="Admin",
        is_admin=True,
        password="scrypt:32768:8:1$jIktSg3PLHmpXNbS$bab47f1d25420d4515fb410729c93d48f8eaa83c07c174391266ff61e780e92265c285d3e93035f852734208ddf02ca5a414e1dcbade4a057ead76c37cfaacfe")
    db.session.add(user)
    db.session.commit()

@admin.before_app_request
def create_admin_user():
    """
    Create an admin user if one doesn't exist.
    """
    if not User.query.filter_by(email="admin@aquametrics.org").first():
        create_admin()

@admin.route("/admin", methods=["GET", "POST"])
@login_required
def admin_page():
    """
    Handle GET and POST requests for the admin page.
    """
    if current_user.is_admin:
        return render_template("admin.html", user=current_user)
    else:
        flash("You do not have permission to access this page.", category="error")
        return redirect(url_for("auth.login"))

# Function to start Serveo and capture the URL
def start_serveo():
    # SSH command to start Serveo
    command = ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:5000", "serveo.net"]

    # Start Serveo and capture the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait for Serveo to establish and capture the output
    for line in process.stdout:
        # Regex to capture the URL
        match = re.search(r'(https://[\w-]+\.serveo\.net)', line)
        if match:
            print(match.group(0))
            return match.group(0)
    
    return None

# Function to send email
def send_email(subject, body, recipient):
    sender = "swimmingmantarain@gmail.com"
    password = "dxnu sgth dbki dmoh "
    
    msg = MIMEText(body, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False

@admin.route("/emails", methods=["POST"])
@login_required
def emails():
    """
    Handle POST requests for sending an email.
    """
    if request.method == "POST":
        recipients = request.form.get("recipients")
        recipients = recipients.split(",")
        link = start_serveo()
        for recipient in recipients:
            subject = "AquaMetrics - Regenerated Link"
            body = f"here is your link:\n{link}"
            send_email(subject, body, recipient)
        
        return redirect(url_for("admin.admin_page"))
