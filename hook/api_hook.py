from datetime import datetime, timedelta
from airflow.providers.http.hooks.http import HttpHook
import requests
import json

# criando classe para herdar as mecânicas de conexão estruturada pelo Airflow no HttpHook
class ApiHook(HttpHook):
    
    def __init__(self, end_time, start_time, query,  conn_id=None):
        self.end_time = end_time
        self.start_time = start_time
        self.query = query
        self.conn_id = conn_id or "api_default"
        super().__init__(http_conn_id=self.conn_id)
    
    def create_url(self):
        # montando url
        TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"

        # passando definição de datas para o HttpHook
        end_time = self.end_time
        start_time = self.start_time

        # recebe a palavra chave de interesse na busca
        query = self.query

        # definindo os campos de retorno no arquivo JSON da API
        tweet_fields = "tweet.fields=author_id,conversation_id,created_at,id,in_reply_to_user_id,public_metrics,lang,text"
        user_fields = "expansions=author_id&user.fields=id,name,username,created_at"

        # URL para fazer a busca com os campos de interesse na visualização
        url_raw = f"{self.base_url}/2/tweets/search/recent?query={query}&{tweet_fields}&{user_fields}&start_time={start_time}&end_time={end_time}"

        return url_raw
    
    def connect_to_endpoint(self, url, session):
        request = requests.Request("GET", url)
        prep = session.prepare_request(request)
        self.log.info(f"URL: {url}")
        return self.run_and_check(session, prep, {})
    
    def paginate(self, url_raw, session):
        lista_json_response = []
        #imprimir json
        response = self.connect_to_endpoint(url_raw, session)
        # leitura da resposta no formato JSON
        json_response = response.json()

        # impressão do JSON no formato string através do dumps com identação e classificado pelas chaves
        lista_json_response.append(json_response)

        # paginação
        contador = 1
        while "next_token" in json_response.get("meta",{}) and contador<10:
            next_token = json_response['meta']['next_token']
            url = f"{url_raw}&next_token={next_token}"
            response = self.connect_to_endpoint(url, session)
            json_response = response.json()
            lista_json_response.append(json_response)
            contador += 1

        return lista_json_response
    
    # método padrão para funcionamento do Hook
    def run(self):
        session = self.get_conn()
        url_raw = self.create_url()

        return self.paginate(url_raw, session)


# garantindo que este código seja executado apenas quando for chamado
if __name__ == "__main__":
    
    # formatando a data que será enviada para API
    TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"

    # capturando a data atual do sistema
    end_time = datetime.now().strftime(TIMESTAMP_FORMAT)

    # utilizando timedelta que permite realizar operações matemáticas com datas
    start_time = (datetime.now() + timedelta(-1)).date().strftime(TIMESTAMP_FORMAT)

    # definindo palavra chave de interesse na busca
    query = "datascience"

    for pg in ApiHook(end_time, start_time, query).run():
        print(json.dumps(pg, indent=4, sort_keys=True))