from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import User
from . import db
import json
import re
from email.mime.text import MIMEText

admin = Blueprint("admin", __name__)

def create_admin():
    user = User(
        email="admin@aquametrics.org",
        firstName="Admin",
        is_admin=True,
        password="scrypt:32768:8:1$jIktSg3PLHmpXNbS$bab47f1d25420d4515fb410729c93d48f8eaa83c07c174391266ff61e780e92265c285d3e93035f852734208ddf02ca5a414e1dcbade4a057ead76c37cfaacfe")
    db.session.add(user)
    db.session.commit()

@admin.before_app_request
def startup_tasks():
    if not User.query.filter_by(email="admin@aquametrics.org").first():
        create_admin()



@admin.route("/admin", methods=["GET", "POST"])
@login_required
def admin_page():
    if current_user.is_admin:
        return render_template("admin.html", user=current_user, coretemps=data[0], temp_avg=data[2], meminfo=data[3], cores=data[1])
    else:
        flash("You do not have permission to access this page.", category="error")
        return redirect(url_for("auth.login"))

"""

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
    if request.method == "POST":
        recipients = request.form.get("recipients")
        recipients = recipients.split(",")
        for recipient in recipients:
            subject = "AquaMetrics - Link"
            body = f"here is your link:\naqua-metrics.serveo.net"
            send_email(subject, body, recipient)
        
        return redirect(url_for("admin.admin_page"))"""
