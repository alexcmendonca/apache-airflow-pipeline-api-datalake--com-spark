import argparse
from os.path import join

from pyspark.sql import SparkSession
from pyspark.sql import functions as f


# função que recebe um df como parâmetro e realiza a transformação
def get_tweet_conversas(df_tweet):
    return df_tweet.alias('tweet')\
            .groupBy(f.to_date('created_at').alias('created_date'))\
            .agg(
                f.countDistinct('author_id').alias('n_tweets'),
                f.sum('like_count').alias('n_like'),
                f.sum('quote_count').alias('n_quote'),
                f.sum('reply_count').alias('n_reply'),
                f.sum('retweet_count').alias('n_retweet')
            ).withColumn('weekday', f.date_format('created_date', 'E'))

# função para salvar os dados transformados
def export_json(df, destino):
    df.coalesce(1).write.mode("overwrite").json(destino)

# função principal agregando a leitura, transformação e gravação
# recebe os parâmetros: spark, origem dos dados, local da gravação e a data q irá acontecer o processamento
def twitter_insight(spark, src, destino, data_processamento):

    # leitura dos dados com o local desejado para leitura
    df_tweet = spark.read.json(join(src, 'tweet'))

    # salvando os dados transformados da camada silver para a camada gold agregados por data
    tweet_conversas = get_tweet_conversas(df_tweet)

    # salvando os dados
    export_json(tweet_conversas, join(destino, f"data_processamento={data_processamento}"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Spark Twitter Transformation Silver"
    )
    parser.add_argument("--src", required=True)
    parser.add_argument("--destino", required=True)
    parser.add_argument("--data_processamento", required=True)
    args = parser.parse_args()

    spark = SparkSession\
        .builder\
        .appName("twitter_transformation")\
        .getOrCreate()

    twitter_insight(spark, args.src, args.destino, args.data_processamento)