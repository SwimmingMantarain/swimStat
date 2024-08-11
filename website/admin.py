from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import User
from . import db
import subprocess
import psutil
import json
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
def startup_tasks():
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
    if request.method == "POST":
        data = request.get_data()
        if data:
            data = data.decode()
            data = re.sub(r'(\w+):', r'"\1":', data)
            data = json.loads(data)
            if data["diag"]:
                return jsonify(getDiagnostics(), 200)
    
    if current_user.is_admin:
        data = getDiagnostics()
        return render_template("admin.html", user=current_user, coretemps=data["temps"], temp_avg=data["temp_avg"], meminfo=data["maminfo"], cores=data["cores"])
    else:
        flash("You do not have permission to access this page.", category="error")
        return redirect(url_for("auth.login"))

def getDiagnostics() -> dict:
    # Core Temps
    command = "sensors | grep Core"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    temps = []
    for line in process.stdout:
        # Tempuratures are printed like this
        # Core 0:         36.0°C (high =  37.0°C, crit =  41.0°C)\n
        # Core 1:         36.0°C (high =  37.0°C, crit =  41.0°C)\n
        match = re.search(r'(\d+\.\d+)', line)
        if match:
            temps.append(match.group(1))
    
    # CPU Individual Core Usage
    cores = []
    command = "cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        try:
            cores.append(float(line) / 1000)
        except ValueError: 
            continue
    # Average CPU Tempurature
    temp_avg = sum([float(temp) for temp in temps]) / len(temps)
    # Memory Usage
    mem_total = psutil.virtual_memory().total / 1024**3  # Total memory in GB
    mem_free = psutil.virtual_memory().available / 1024**3  # Available memory in GB
    mem_buffers = psutil.virtual_memory().buffers / 1024**3  # Buffers in GB
    mem_cached = psutil.virtual_memory().cached / 1024**3  # Cached memory in GB
    meminfo = [mem_total, mem_free + mem_buffers + mem_cached, mem_free]

    return {
        "temps": temps,
        "temp_avg": temp_avg,
        "meminfo": meminfo,
        "cores": cores
    }

"""
# Function to start Serveo and capture the URL
def start_serveo():
    # Kill any existing Serveo processes
    subprocess.run(["killall", "ssh"])

    # SSH command to start Serveo
    command = ["ssh", "-R", "aqua-metrics:80:localhost:80", "serveo.net"]

    # Start Serveo and capture the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait for Serveo to establish and capture the output
    for line in process.stdout:
        # Regex to capture the URL
        match = re.search(r'(https://aqua-metrics\.serveo\.net)', line)
        if match:
            return match.group(0)
    
    return None"""

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
        #link = start_serveo()
        for recipient in recipients:
            subject = "AquaMetrics - Regenerated Link"
            body = f"here is your link:\naqua-metrics.serveo.net"
            send_email(subject, body, recipient)
        
        return redirect(url_for("admin.admin_page"))
