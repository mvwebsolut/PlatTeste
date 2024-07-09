from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import User
from app.extensions import database as db
from app.forms import LoginForm, RegisterForm

router = Blueprint("auth", __name__, url_prefix='/auth')


@router.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    else:
        return redirect(url_for("auth.login"))


@router.route("/login", methods=["POST", "GET"])
def login():
    login_form = LoginForm()

    if request.method == "POST" and login_form.validate_on_submit():

        email_address = login_form.email_field.data
        password = login_form.password_field.data

        user = User.query.filter_by(email=email_address).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for("home.index"))
        else:
            flash("Usuário ou senha inválidos.", "error")
            return redirect(url_for("auth.login"))
    else:
        return render_template("login.html", form=login_form)


@router.route("/register", methods=["POST", "GET"])
def register():
    register_form = RegisterForm()

    if request.method == "POST":

        print("validado")

        fullname = register_form.fullname_field.data
        email_address = register_form.email_field.data
        password = register_form.password_field.data

        user = User.query.filter_by(email=email_address).first()
        if not user:
            new_user = User(
                fullname=fullname,
                email=email_address,
                password=generate_password_hash(password)
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=True)
                return redirect(url_for("home.index"))
            except Exception as error:
                print(f"Erro ao registrar usuário, {str(error)}")
                db.session.rollback()
                flash("Erro interno ao cadastrar usuário", "error")
                return redirect(url_for("auth.register"))
        else:
            flash("Usuário já cadastrado no sistema.", "error")
            return redirect(url_for("auth.login"))
    else:
        return render_template("register.html", form=register_form)


@router.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso.", "success")
    return redirect(url_for("auth.login"))
