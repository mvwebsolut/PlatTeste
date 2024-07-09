from flask import Blueprint, request, url_for, jsonify
from datetime import datetime

from app.extensions import database
from app.models import Person, Address
from app.modules.sus_api import SUSApi

router = Blueprint("webhooks", __name__, url_prefix='/webhooks')
sus_api = SUSApi()

@router.route('/')
def index():
    return "Webhooks Page !"


@router.route('/add_person', methods=['POST'])
def add_person():
    person_json_data = request.json

    check_user = Person.query.filter_by(cpf=person_json_data['cpf']).first()

    if check_user:
        data = dict(
            success=False,
            message="pessoa já foi cadastrada no banco de dados."
        )
        return jsonify(data), 400

    person = Person()
    person.name = person_json_data['nome']
    person.cpf = person_json_data['cpf']
    person.mother_name = person_json_data['nomeMae']

    try:
        person.father_name = person_json_data['nomePai']
    except KeyError:
        person.father_name = "undefined"

    person.is_dead = person_json_data['obito']
    person.birthday = datetime.strptime(person_json_data['dataNascimento'], "%Y-%m-%d")

    sex = person_json_data['sexo']

    if sex == "F":
        person.sex = "female"
    elif sex == "M":
        person.sex = "male"
    else:
        person.sex = "undefined"

    try:
        born_country_id = person_json_data['nacionalidade']['municipioNascimento']
        born_country = sus_api.get_district(born_country_id)['record']['nome']
    except Exception as error:
        print("Erro ao buscar o municipio de nascimento na api.")
        born_country = "undefined"

    person.born_country = born_country

    try:
        nationality_id = person_json_data['nacionalidade']['paisNascimento']
        nationality = sus_api.get_nationality(nationality_id)['nome']
    except Exception as error:
        print("Erro ao buscar a nacionalidade na api.")
        nationality = "undefined"

    person.nationality = nationality

    try:
        race_id = person_json_data['racaCor']
        race = sus_api.get_race(race_id)['descricao']
    except Exception as error:
        print("Erro ao buscar a raça na api.")
        race = "undefined"

    person.race = race

    if person_json_data['endereco']:
        address = Address()
        address.street = person_json_data['endereco']['logradouro']
        address.number = person_json_data['endereco']['numero']
        address.district = person_json_data['endereco']['bairro']
        address.uf = person_json_data['endereco']['siglaUf']

        try:
            country_id = person_json_data['endereco']['pais']
            country = sus_api.get_country(country_id)['nome']
        except Exception as error:
            print("Erro ao buscar o pais na api.")
            country = "undefined"

        address.country = country
        address.cep = person_json_data['endereco']['cep']

        try:
            municipe_id = person_json_data['endereco']['municipio']
            municipe = sus_api.get_district(municipe_id)['record']['nome']
        except Exception as error:
            print(error)
            print("Erro ao buscar o municipio na api.")
            municipe = "undefined"

        address.municipe = municipe

        person.addresses.append(address)

    try:
        database.session.add(person)
        database.session.commit()
        print(f"Pessoa com o cpf {person.cpf} salva com sucesso.")
        return jsonify(dict(
            success=True,
            message=f"Pessoa com o cpf {person.cpf} salva com sucesso."
        )), 201
    except Exception as error:
        print(error)
        return jsonify(dict(
            success=True,
            message=f"Erro ao salvar pessoa com o cpf {person.cpf}."
        )), 400








    






