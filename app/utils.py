from app.extensions import database as db
from app.models import Person, Address

from sqlalchemy import func, case, extract


def format_persons_to_table(perons):
    persons_list = []
    for person in perons:
        data = [person.name, person.cpf, person.birthday.strftime("%d/%m/%Y"), person.mother_name, person.use_pix,
                "true" if person.use_betano else "false", person.receipt_status, "Morto" if person.is_dead else "Vivo"]
        persons_list.append(data)
    return persons_list


def get_persons_etari():
    faixas_etarias = ['0-14', '14-25', '25-50', '50-75', '75-99']
    resultados = []

    for faixa in faixas_etarias:
        inicio, fim = map(int, faixa.split('-'))

        # Calcular a idade usando funções do SQLAlchemy
        query = db.session.query(func.count(Person.id)).filter(
            extract('year', func.now()) - extract('year', Person.birthday) >= inicio,
            extract('year', func.now()) - extract('year', Person.birthday) <= fim
        ).scalar()

        resultados.append(query or 0)

    return resultados


def get_daily_added_count():
    result = db.session.query(
        extract('year', Person.crt_att).label('year'),
        extract('month', Person.crt_att).label('month'),
        func.count(Person.id).label('count')
    ).group_by('year', 'month').order_by('year', 'month').all()

    data = []
    for row in result:
        # Criar objeto de data no formato aceito pelo ApexCharts
        data.append(row.count)

    return data


def get_district_woman_and_man_ammount():
    estados_habitantes = db.session.query(
        Address.uf,
        func.count(Person.id).label('total_habitantes'),
        func.sum(case((Person.sex == 'male', 1), else_=0)).label('homens'),
        func.sum(case((Person.sex == 'female', 1), else_=0)).label('mulheres')
    ).join(Person, Address.person_id == Person.id).group_by(Address.uf).all()

    nomes_estados = [estado.uf for estado in estados_habitantes]
    habitantes_homens = [estado.homens for estado in estados_habitantes]
    habitantes_mulheres = [estado.mulheres for estado in estados_habitantes]

    chart_data = {
        "nomes_estados": nomes_estados,
        "habitantes_homens": habitantes_homens,
        "habitantes_mulheres": habitantes_mulheres
    }

    return chart_data
