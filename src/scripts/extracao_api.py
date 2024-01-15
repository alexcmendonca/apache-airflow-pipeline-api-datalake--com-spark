from datetime import datetime, timedelta
import requests
import json
import os
from dotenv import load_dotenv

# formatando a data que será enviada para API
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"

# capturando a data atual do sistema
end_time = datetime.now().strftime(TIMESTAMP_FORMAT)

# utilizando timedelta que permite realizar operações matemáticas com datas
start_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP_FORMAT)

# definindo palavra chave de interesse na busca
query = "datascience"

# passando os campos de interesse no arquivo JSON que a API irá retornar
tweet_fields = "tweet.fields=author_id,conversation_id,created_at,id,in_reply_to_user_id,public_metrics,lang,text"
user_fields = "expansions=author_id&user.fields=id,name,username,created_at"

# definindo URL para fazer a busca com os campos de interesse na visualização
url_raw = f"https://labdados.com/2/tweets/search/recent?query={query}&{tweet_fields}&{user_fields}&start_time={start_time}&end_time={end_time}"

# Carrega as variáveis do arquivo .env no ambiente de trabalho
load_dotenv()
bearer_token = os.getenv('token')
headers = {'Authorization': 'Bearer {}'.format(bearer_token)}

# requisição GET para url com o cabecalho
response = requests.request("GET", url_raw, headers=headers)

# leitura da resposta no formato JSON
json_response = response.json()

# impressão do JSON no formato string através do dumps com identação e classificado pelas chaves
print(json.dumps(json_response, indent=4, sort_keys=True))

# paginação
while "next_token" in json_response.get("meta",{}):
    next_token = json_response['meta']['next_token']
    url = f"{url_raw}&next_token={next_token}"
    response = requests.request("GET", url, headers=headers)
    json_response = response.json()
    print(json.dumps(json_response, indent=4, sort_keys=True))