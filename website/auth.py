from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle POST and GET requests for user login.
    """
    if request.method == "POST":
        # Get email and password from form
        email = request.form.get("email")
        password = request.form.get("password")

        if email == "admin@aquametrics.org":
            user = User.query.filter_by(email=email).first()
            if user.is_admin:
                if check_password_hash(user.password, password):
                    flash("Logged in successfully.", category="success")
                    login_user(user, remember=True)
                    return redirect(url_for("admin.admin_page"))
                else:
                    flash("Incorrect password, try again.", category="error")

        # Check if user exists and password is correct
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully.", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Incorrect email, email isn't registered.", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    """
    Logout the user and redirect to login page.
    """
    logout_user()
    flash("Logged Out", category="success")
    return redirect(url_for("auth.login"))

@auth.route("/sign-up",  methods=["GET", "POST"])
def sign_up():
    """
    Handle POST and GET requests for user sign up.
    """
    if request.method == "POST":
        # Get user details from form
        email = request.form.get("email")
        firstName = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Check if email is already registered
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already registered.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(firstName) < 2:
            flash("First name must be greater than 1 characters.", category="error")
        elif password1 != password2:
            flash("Passwords must match!", category="error")
        elif len(password1) < 8:
            flash("Password must be at least 8 characters.", category="error")
        else:
            # Create new user and log them in
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, "scrypt"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created.", category="success")
            return redirect(url_for("views.home"))
    
    return render_template("sign_up.html", user=current_user)