import base64
import requests

class SUSApi:

    def __init__(self):
        self.user = "vanessarochatriches93@gmail.com:esus2021"
        self.user_basic = base64.b64encode(self.user.encode()).decode()
        self.get_bearer_url = "https://servicos-cloud.saude.gov.br/pni-bff/v1/autenticacao/tokenAcesso"
        self.consult_url = "https://servicos-cloud.saude.gov.br/pni-bff/v1/"
        self.bearer_token = None
        self.refresh_token = None
        self.get_bearer_token()
        self.ufs_codes = [{"codigo": "12", "nome": "ACRE", "sigla": "AC", "codigoPais": 1, "codigoRegiao": "1"},
                          {"codigo": "27", "nome": "ALAGOAS", "sigla": "AL", "codigoPais": 1, "codigoRegiao": "2"},
                          {"codigo": "13", "nome": "AMAZONAS", "sigla": "AM", "codigoPais": 1, "codigoRegiao": "1"},
                          {"codigo": "16", "nome": "AMAPÁ", "sigla": "AP", "codigoPais": 1, "codigoRegiao": "1"},
                          {"codigo": "29", "nome": "BAHIA", "sigla": "BA", "codigoPais": 1, "codigoRegiao": "2"},
                          {"codigo": "23", "nome": "CEARÁ", "sigla": "CE", "codigoPais": 1, "codigoRegiao": "2"},
                          {"codigo": "53", "nome": "DISTRITO FEDERAL", "sigla": "DF", "codigoPais": 1,
                           "codigoRegiao": "5"},
                          {"codigo": "32", "nome": "ESPÍRITO SANTO", "sigla": "ES", "codigoPais": 1,
                           "codigoRegiao": "3"},
                          {"codigo": "52", "nome": "GOIÁS", "sigla": "GO", "codigoPais": 1, "codigoRegiao": "5"},
                          {"codigo": "21", "nome": "MARANHÃO", "sigla": "MA", "codigoPais": 1, "codigoRegiao": "2"},
                          {"codigo": "31", "nome": "MINAS GERAIS", "sigla": "MG", "codigoPais": 1, "codigoRegiao": "3"},
                          {"codigo": "50", "nome": "MATO GROSSO DO SUL", "sigla": "MS", "codigoPais": 1,
                           "codigoRegiao": "5"},
                          {"codigo": "51", "nome": "MATO GROSSO", "sigla": "MT", "codigoPais": 1, "codigoRegiao": "5"},
                          {"codigo": "15", "nome": "PARÁ", "sigla": "PA", "codigoPais": 1, "codigoRegiao": "1"},
                          {"codigo": "25", "nome": "PARAÍBA", "sigla": "PB", "codigoPais": 1, "codigoRegiao": "2"},
                          {"codigo": "26", "nome": "PERNAMBUCO", "sigla": "PE", "codigoPais": 1, "codigoRegiao": "2"},
                          {"codigo": "22", "nome": "PIAUÍ", "sigla": "PI", "codigoPais": 1, "codigoRegiao": "2"},
                          {"codigo": "41", "nome": "PARANÁ", "sigla": "PR", "codigoPais": 1, "codigoRegiao": "4"},
                          {"codigo": "33", "nome": "RIO DE JANEIRO", "sigla": "RJ", "codigoPais": 1,
                           "codigoRegiao": "3"},
                          {"codigo": "24", "nome": "RIO GRANDE DO NORTE", "sigla": "RN", "codigoPais": 1,
                           "codigoRegiao": "2"},
                          {"codigo": "11", "nome": "RONDÔNIA", "sigla": "RO", "codigoPais": 1, "codigoRegiao": "1"},
                          {"codigo": "14", "nome": "RORAIMA", "sigla": "RR", "codigoPais": 1, "codigoRegiao": "1"},
                          {"codigo": "43", "nome": "RIO GRANDE DO SUL", "sigla": "RS", "codigoPais": 1,
                           "codigoRegiao": "4"},
                          {"codigo": "42", "nome": "SANTA CATARINA", "sigla": "SC", "codigoPais": 1,
                           "codigoRegiao": "4"},
                          {"codigo": "28", "nome": "SERGIPE", "sigla": "SE", "codigoPais": 1, "codigoRegiao": "2"},
                          {"codigo": "35", "nome": "SÃO PAULO", "sigla": "SP", "codigoPais": 1, "codigoRegiao": "3"},
                          {"codigo": "17", "nome": "TOCANTINS", "sigla": "TO", "codigoPais": 1, "codigoRegiao": "1"},
                          {"codigo": "XX", "nome": "INVÁLIDA", "sigla": "XX"}]

    def get_bearer_token(self):

        response = requests.post(
            url=self.get_bearer_url,
            headers={
                'accept': 'application/json',
                'DNT': '1',
                'Referer': 'https://si-pni.saude.gov.br/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                'X-Authorization': f'Basic {self.user_basic}',
            },
            data=None
        )

        if response.status_code == 200:
            try:
                access_token = response.json()['accessToken']
                refresh_token = response.json()['refreshToken']
                self.bearer_token = access_token
                self.refresh_token = refresh_token
                print("tokens obtidos com sucesso.")
            except KeyError:
                print(f"ocorreu um erro ao tentar autenticar o usuário ao sus, {response.json()}")
        else:
            print(f"ocorreu um erro ao tentar autenticar o usuário ao sus, {response.json()}")

    def get_district(self, id):
        url = self.consult_url + f'municipio/{id}'
        response = requests.get(
            url=url,
            headers={
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
                'Accept': 'application/json, text/plain, */*',
                'Referer': 'https://si-pni.saude.gov.br/',
                'Origin': 'https://si-pni.saude.gov.br',
                'Host': 'servicos-cloud.saude.gov.br',
                'sec-ch-ua-mobile': '?0',
                'Authorization': f'Bearer {self.bearer_token}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
                'sec-ch-ua-platform': '"Windows"',
            }
        )

        if response.status_code == 200:
            return response.json()
        else:
            return "Não Disponível - Não Disponível"

    def get_countries_codes(self, uf_code: str):
        url = self.consult_url + f'municipio?codigoUf={uf_code}'
        response = requests.get(
            url=url,
            headers={
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
                'Accept': 'application/json, text/plain, */*',
                'Referer': 'https://si-pni.saude.gov.br/',
                'sec-ch-ua-mobile': '?0',
                'Authorization': f'Bearer {self.bearer_token}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
                'sec-ch-ua-platform': '"Windows"',
            }
        )

        if response.status_code == 200:
            try:
                print(f"conslta ao estado {response.json()['records'][0]['siglaUf']} feita com sucesso.")
                return response.json()['records']
            except KeyError:
                print(f"ocorreu um erro ao tentar autenticar o usuário ao sus, {response.json()}")
        else:
            print(f"ocorreu um erro ao tentar autenticar o usuário ao sus, {response.json()}")

    def get_nationality(self, country_code: str):
        url = self.consult_url + f'pais/{country_code}'
        response = requests.get(
            url=url,
            headers={
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
                'Accept': 'application/json, text/plain, */*',
                'Referer': 'https://si-pni.saude.gov.br/',
                'sec-ch-ua-mobile': '?0',
                'Authorization': f'Bearer {self.bearer_token}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
                'sec-ch-ua-platform': '"Windows"',
            }
        )

        if response.status_code == 200:
            try:
                print(f"conslta ao pais {response.json()['record']['nome']} feita com sucesso.")
                return response.json()['record']
            except KeyError:
                print(f"ocorreu um erro ao tentar autenticar o usuário ao sus, {response.json()}")
        else:
            print(f"ocorreu um erro ao tentar autenticar o usuário ao sus, {response.json()}")

    def get_race(self, race_code: str):
        url = self.consult_url + f'racacor/{race_code}'
        response = requests.get(
            url=url,
            headers={
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
                'Accept': 'application/json, text/plain, */*',
                'Referer': 'https://si-pni.saude.gov.br/',
                'sec-ch-ua-mobile': '?0',
                'Authorization': f'Bearer {self.bearer_token}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
                'sec-ch-ua-platform': '"Windows"',
            }
        )

        if response.status_code == 200:
            try:
                print(f"conslta a raça {response.json()['record']['descricao']} feita com sucesso.")
                return response.json()['record']
            except KeyError:
                print(f"ocorreu um erro ao tentar autenticar o usuário ao sus, {response.json()}")
        else:
            print(f"ocorreu um erro ao tentar autenticar o usuário ao sus, {response.json()}")

    def get_country(self, country_code: str):
        url = self.consult_url + f'pais/{country_code}'
        response = requests.get(
            url=url,
            headers={
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
                'Accept': 'application/json, text/plain, */*',
                'Referer': 'https://si-pni.saude.gov.br/',
                'sec-ch-ua-mobile': '?0',
                'Authorization': f'Bearer {self.bearer_token}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
                'sec-ch-ua-platform': '"Windows"',
            }
        )

        if response.status_code == 200:
            try:
                print(f"conslta ao pais {response.json()['record']['nome']} feita com sucesso.")
                return response.json()['record']
            except KeyError:
                print(f"ocorreu um erro ao tentar autenticar o usuário ao sus, {response.json()}")
        else:
            print(f"ocorreu um erro ao tentar autenticar o usuário ao sus, {response.json()}")

