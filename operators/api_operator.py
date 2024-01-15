import sys
from airflow.models import BaseOperator, DAG, TaskInstance
from datetime import datetime, timedelta

sys.path.insert(0, '/home/alex/Documents/airflow')


from hook.api_hook import ApiHook
import json
from os.path import join
from pathlib import Path

class ApiOperator(BaseOperator):

    template_fields = ['query', 'file_path', 'start_time', 'end_time']

    # criando método construtor
    def __init__(self, file_path, end_time, start_time, query, **kwargs):
        self.end_time = end_time
        self.start_time = start_time
        self.query = query
        self.file_path = file_path
        # garantindo o funcionamento essencial do operador do Airflow seja tratado antes de código do ApiOperator
        super().__init__(**kwargs)
    
    def create_parent_folder(self):
        (Path(self.file_path).parent).mkdir(parents=True, exist_ok=True)


    # definindo método principal que faz parte do BaseOperator passando info padrão que o DAG precisa
    def execute(self, context):
        end_time = self.end_time
        start_time = self.start_time
        query = self.query
        self.create_parent_folder()
        # salvando os dados JSON em um arquivo
        with open(self.file_path, 'w') as output_file:
            for pg in ApiHook(end_time, start_time, query).run():
                json.dump(pg, output_file, ensure_ascii=False)
                output_file.write('\n')

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

    # criando um DAG passando os parâmetros principais
    with DAG(
        dag_id = 'ApiTest', 
        start_date=datetime.now()
        ) as dag:
        # criando as tarefas instanciando as duas classes abaixo
        to = ApiOperator(file_path=join('datalake/api_datascience',
                                    f'extract_date={datetime.now().date()}',
                                    f'datascience_{datetime.now().date().strftime("%Y%m%d")}.json'),
                                    query=query, start_time=start_time, end_time=end_time, task_id='test_run')
        # taskeIntance representa uma execução específica de uma tarefa dentro de um DAG
        ti = TaskInstance(task=to)
        to.execute(ti.task_id)