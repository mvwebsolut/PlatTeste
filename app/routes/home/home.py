from flask import Blueprint, jsonify, render_template, request
from flask_login import current_user, login_required

from app.models import Person, Address
from app.schemas import PersonsSchema, AddressessSchema, MunicipeSchema
from app.extensions import database as db
from app.utils import get_district_woman_and_man_ammount, get_daily_added_count, get_persons_etari, \
    format_persons_to_table

router = Blueprint("home", __name__, url_prefix='/')


@router.route('/')
@login_required
def index():
    persons = Person.query.all()
    chart_one_data = get_district_woman_and_man_ammount()
    daily_count_data = get_daily_added_count()
    etary_of_persons = get_persons_etari()
    person_table = format_persons_to_table(persons)
    with_pix_amount = len(Person.query.filter_by(use_pix=1).all())
    no_pix_amount = len(Person.query.filter_by(use_pix=2).all())
    return render_template("index.html", with_pix_amount=with_pix_amount, no_pix_amount=no_pix_amount, index="home",
                           persons=persons, chart_one=chart_one_data, daily_count=daily_count_data,
                           etary=etary_of_persons, person_table=person_table)


@router.route('/update_data_status/<cpf>', methods=['POST'])
def update_data_status(cpf):

    if request.headers['x-token'] != "bot":
        return jsonify({"error":  True, "message": "Unalthorized access."}), 500

    person = Person.query.filter_by(cpf=cpf).first()
    if not person:
        return jsonify({"error": True, "message": "Dados não encontrados."}), 400

    data = request.json

    try:
        use_betano = int(data['use_betano'])
        person.use_betano = use_betano
    except KeyError:
        pass


    try:
        receipt_status = int(data['receipt_status'])
        person.receipt_status = receipt_status
    except KeyError:
        pass

    try:
        use_pix = int(data['use_pix'])
        person.use_pix = use_pix
    except KeyError:
        pass

    try:
        db.session.commit()
        print("Dados atualizado com sucesso.")
        return jsonify({"error": False, "message": "dados atualizado com sucesso."}), 200
    except Exception as error:
        print("Erro ao atualizar informações dos dados.")
        print(str(error))
        db.session.rollback()
        return jsonify({"error": True, "message": "erro ao atualizar os dados."}), 500

@router.route("/purchase_datas")
@login_required
def purchased_data():
    # datas = current_user.owned_datas
    pessoas = Person.query.all()
    person_table = format_persons_to_table(pessoas)
    return render_template("purchase_datas.html", person_table=person_table, index="purchase_datas")


@router.route("/my_datas")
@login_required
def my_purchased_datas():
    datas = current_user.owned_datas
    person_table = format_persons_to_table(datas)
    return render_template("my_datas.html", person_table=person_table, index="my_datas")


@router.route("/get_person/<cpf>")
@login_required
def get_person(cpf):
    user = Person.query.filter_by(cpf=cpf).first()
    user_schema = PersonsSchema()
    return jsonify(user_schema.dump(user))


@router.route('/municipe', methods=['GET'])
@login_required
def get_municipes():
    municipies = db.session.query(Address.municipe).distinct().all()
    schema = MunicipeSchema(many=True)
    return jsonify(schema.dump(municipies))
