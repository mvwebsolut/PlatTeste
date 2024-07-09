from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired


class LoginForm(FlaskForm):
    email_field = EmailField("E-mail", validators=[Email(), DataRequired("Por favor digite um e-mail.")])
    password_field = PasswordField("Password", validators=[DataRequired("Por favor digite uma senha.")])
    remember_field = BooleanField("remember_me")
    login_button = SubmitField("Login")


class RegisterForm(FlaskForm):
    fullname_field = StringField("Fullname", validators=[DataRequired("Por favor digite o seu nome completo.")])
    email_field = EmailField("E-mail", validators=[Email(), DataRequired("Por favor digite um e-mail válido.")])
    password_field = PasswordField("Password", validators=[DataRequired("Por favor digite uma senha."),
                                                           EqualTo("Rept Password", "Senha não são iguais.")])
    rept_password_field = PasswordField("Rept Password", validators=[DataRequired("Por favor digite uma senha.")])
    terms_field = BooleanField("Terms")
    register_button = SubmitField("Registrar-se")
