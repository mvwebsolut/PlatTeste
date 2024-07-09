from datetime import datetime

from flask_login import UserMixin
from app.extensions import database as db
from app.extensions import login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    owned_datas = db.relationship("Person", backref="user")
    crt_att = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())


class Address(db.Model):
    __tablename__ = "addresses"
    id = db.Column(db.Integer, primary_key=True)

    street = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(255))
    district = db.Column(db.String(255))
    municipe = db.Column(db.String(255))
    country = db.Column(db.String(255))
    uf = db.Column(db.String(255))
    cep = db.Column(db.String(255))

    person_id = db.Column(db.Integer, db.ForeignKey("persons.id"), nullable=False)
    person = db.relationship("Person", back_populates="addresses")


class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    birthday = db.Column(db.DateTime(), nullable=False)
    cpf = db.Column(db.String(255), nullable=False, unique=True)

    mother_name = db.Column(db.String(255))
    father_name = db.Column(db.String(255))

    is_dead = db.Column(db.Boolean, default=False)
    sex = db.Column(db.String(255), nullable=False)
    race = db.Column(db.String(255))

    born_country = db.Column(db.String(255))
    nationality = db.Column(db.String(255))

    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    crt_att = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())

    addresses = db.relationship("Address", back_populates="person")
    use_pix = db.Column(db.Integer, default=0)
    receipt_status = db.Column(db.Integer, default=0)
    use_betano = db.Column(db.Integer, default=0)
    verified_by_bot = db.Column(db.Boolean, default=False)


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()
