import sys
sys.path.insert(0, '/home/alex/Documents/airflow')
from airflow.models import DAG
from datetime import datetime, timedelta
from operators.api_operator import ApiOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from os.path import join
from airflow.utils.dates import days_ago
from pathlib import Path

with DAG(
        dag_id = 'ApiDAG', 
        start_date = days_ago(2),
        schedule_interval = '@daily'
        ) as dag:

        BASE_FOLDER = join(
                str(Path("~/Documents").expanduser()),
                "airflow/datalake/{stage}/api_datascience/{partition}",
        )
        PARTITION_FOLDER_EXTRACT = "extract_date={{ data_interval_start.strftime('%Y-%m-%d') }}"


        TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.00Z"
        query = "datascience"
        twitter_operator = ApiOperator(file_path=join(BASE_FOLDER.format(stage='bronze', partition=PARTITION_FOLDER_EXTRACT),
                                    'datascience_{{ ds_nodash }}.json'),
                                    query=query, 
                                    start_time='{{ data_interval_start.strftime("%Y-%m-%dT%H:%M:%S.00Z") }}', 
                                    end_time='{{ data_interval_end.strftime("%Y-%m-%dT%H:%M:%S.00Z") }}', 
                                    task_id='twitter_datascience')
        
        twitter_transform = SparkSubmitOperator(task_id='transform_twitter_datascience',
                                                application='/home/alex/Documents/airflow/src/spark/transformation.py',
                                                name='twitter_transformation',
                                                application_args=['--src', BASE_FOLDER.format(stage='bronze', partition=PARTITION_FOLDER_EXTRACT),
                                                                  '--destino', BASE_FOLDER.format(stage='silver', partition=''),
                                                                  '--data_processamento', '{{ ds }}'])
        
        twitter_insight = SparkSubmitOperator(task_id="insights_twitter",
                                            application="/home/alex/Documents/airflow/src/spark/insights_tweet.py",
                                            name="insights_twitter",
                                            application_args=["--src", BASE_FOLDER.format(stage="silver", partition=""),
                                             "--destino", BASE_FOLDER.format(stage="gold", partition=""),
                                             "--data_processamento", "{{ ds }}"])


twitter_operator >> twitter_transform >> twitter_insight