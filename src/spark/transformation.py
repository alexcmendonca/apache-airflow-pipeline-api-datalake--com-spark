from pyspark.sql import functions as f
from pyspark.sql import SparkSession
from os.path import join
import argparse

# funcao para extrair dados do dataframe e salvar info em um novo df só de tweet
def get_tweets_data(df):
    tweet_df = df.select(f.explode("data").alias("tweets"))\
        .select("tweets.author_id", "tweets.conversation_id",
        "tweets.created_at", "tweets.id",
        "tweets.public_metrics.*", "tweets.text")
    return tweet_df

# função para extrair dados dos usuários
def get_users_data(df):
    user_df = df.select(f.explode("includes.users").alias("users")).select("users.*")
    return user_df

# função para armazenar os dados
def export_json(df, destino):
    df.coalesce(1).write.mode("overwrite").json(destino)

# função global de modo genérico com todas as funções
# responsabilidade de quem utilizar função para definir origem dos dados
# responsabilidade do Airflow para criar sessão Spark
def twitter_transformation(spark, src, destino, data_processamento):
    df = spark.read.json(src)

    tweet_df = get_tweets_data(df)
    user_df = get_users_data(df)

    tabela_destino = join(destino, '{table_name}', f'data_processamento={data_processamento}')

    export_json(tweet_df, tabela_destino.format(table_name='tweet'))
    export_json(user_df, tabela_destino.format(table_name='user'))

# definindo uma condicional para garantir que o código abaixo seja executado primeiro ao rodar o script
if __name__ == '__main__':

    # utilizando módulo 'argparse' para o script aceitar argumentos obrigatórios via linha de comando
    parser = argparse.ArgumentParser(
        description='Spark Twitter Transformation'
    )
    parser.add_argument("--src", required=True)
    parser.add_argument("--destino", required=True)
    parser.add_argument("--data_processamento", required=True)

    args = parser.parse_args()

    spark = SparkSession\
    .builder\
    .appName('api_transformation')\
    .getOrCreate()

    twitter_transformation(spark, args.src, args.destino, args.data_processamento)


