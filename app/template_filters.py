from flask import jsonify

from app.extensions import database
from app.models import Person, Address

def get_states_from_db(a):
    db_states = database.session.query(Address.municipe).distinct().all()
    municipies = [str(data[0]) for data in db_states]
    return municipies