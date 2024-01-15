# Desenvolvimento de um Pipeline de Dados em Python dedicado à extração de informações através de uma API. Utilizando as poderosas ferramentas Apache Airflow para orquestração do fluxo de dados e Apache Spark para realizar extração e transformações robustas nos conjuntos de dados.

## 💡Objetivos
O objetivo deste projeto é aprimorar o projeto "Desenvolvimento de um Pipeline de Dados em Python para extração de dados via API utilizando o Apache Airflow" [https://github.com/alexcmendonca/apache-airflow-pipeline-api-datalake]. Esta atualização incorpora a ferramenta Spark para aprimorar a transformação dos dados, introduzindo uma nova estrutura ao Data Lake com a implementação de uma arquitetura de medalhas. Ao término do projeto, os dados serão entregues de maneira organizada, facilitando sua interpretação.

###### Imagem 1: Diagrama final do Pipeline deste Projeto (Créditos da imagem: Alura)
<img src="/assets/img/img-pipeline-final.png">


## 🖥️Desafios do Projeto
Empregar a integração do Apache Airflow com Spark, PySpark e o operador Spark Submit para efetuar a transformação dos dados e promover a reestruturação do Data Lake por meio de uma arquitetura baseada em medalhas. Esse enfoque fragmentará as etapas em distintas camadas, configurando as três camadas como a nova estrutura aplicada ao Data Lake. Essa abordagem não apenas proporcionará maior organização ao ambiente, mas também viabilizará a refinamento dos dados brutos de maneira mais eficiente.

###### Imagem 2: Diagrama final do Pipeline deste Projeto (Créditos da imagem: Alura)
<img src="/assets/img/arquitetura_medalhao.png">

**- Resumo da execução do Projeto**

Reestruturação do Data Lake adotando uma arquitetura de medalhão composta por três camadas: Bronze, Silver e Gold. Essa abordagem visa conferir maior organização ao Data Lake, proporcionando suporte eficaz para o refinamento dos dados brutos.

A exploração detalhada dos dados ocorreu por meio do Spark / PySpark, utilizando o arquivo Jupyter Notebook denominado "exploracao_spark.ipynb". Durante a análise dos dados, foram identificadas as informações essenciais e aquelas que deveriam ser descartadas. Com base nessas conclusões, procedemos à separação dos dados relevantes, simplificando a interpretação dos conjuntos de dados. A aplicação dos métodos select e explode possibilitou a extração precisa dos dados relacionados a tweets e usuários, sendo posteriormente armazenados em um novo DataFrame.

Transformamos a exploração de dados realizada no Jupyter Notebook em um script Python denominado "transformation.py", o qual será posteriormente integrado ao pipeline orquestrado pelo Apache Airflow.
	Funções desenvolvidas:
		**get_tweets_data():** Encarregada de extrair os dados brutos do DataFrame e criar um novo contendo exclusivamente os tweets.
		get_users_data(df): Utilizada para extrair informações relacionadas aos usuários.
		export_json(): Responsável por salvar e armazenar os dados resultantes.
		twitter_transformation(): Função principal que incorpora Spark, englobando todas as funções. Realiza a leitura do DataFrame original e invoca as funções de extração e salvamento, consolidando assim a transformação dos dados.

Testamos o script Python "transformation.py" utilizando o Spark Submit.

Instalação e utilização do Operador Spark, especificamente o "SparkSubmitOperator", na atualização do arquivo de Dags, denominado "api_dag.py". Nessa atualização, foi criado um novo operador dedicado à transformação dos dados e à gravação dos resultados.

Para estabelecer a conexão entre o Apache Airflow e o Spark, editamos a conexão preexistente chamada "spark_default". Esse ajuste foi realizado por meio da interface web do Airflow, acessível pela seção "Admin" na barra superior, selecionando a opção "Connections".

Executamos o Apache Airflow, agora com a DAG devidamente atualizada, o que resultou na gravação dos dados transformados no diretório "dados_transformation".

Aprimorando o Projeto com a Reestruturação do Data Lake e Refatoração do Código da DAG.

	1. Reorganização do Data Lake em Duas Camadas (Bronze e Silver): Para efetuar essa modificação, procedemos com a atualização da Directed Acyclic Graph (DAG), corrigindo caminhos e pastas para alinhar-se com os objetivos do projeto.

	2. Aprimoramento da Dinamicidade e Centralização da Estrutura do Data Lake: Implementamos medidas que garantem a dinamicidade e centralização da estrutura do Data Lake. Para isso, introduzimos duas variáveis cruciais:
                - BASE_FOLDER: Utilizada como referência para o caminho do Data Lake, tornando desnecessário lembrar de todos os pontos que precisam ser alterados em caso de modificação.
                - PARTITION_FOLDER_EXTRACT: Responsável por retornar a data de início da extração (extract_date), proporcionando uma abordagem mais eficiente.
        
        Essas atualizações visam otimizar a manutenção e evolução contínua do projeto, conferindo-lhe maior flexibilidade e praticidade.

Inclusão de nova demanda no projeto: adicionando uma nova etapa no pipeline. Além do desenvolvimento da extração de dados, implementamos uma fase adicional para realizar a transformação desses dados. Essa transformação tem como objetivo gerar um novo conjunto de dados que irá apoiar o desenvolvimento de um relatório específico. Nessa nova etapa, o foco foi na extração dos valores relacionados à data em que os tweets foram postados.

Essa abordagem permitiu visualizar o desempenho da palavra-chave "data science" nos tweets de forma mais específica e detalhada. Resumindo, a ideia foi utilizar os dados já coletados até o momento na etapa de extração e, agora, aplicando uma transformação, consolidando essas informações por dia da semana. Essa estratégia proporcionará uma análise mais refinada e direcionada ao aspecto temporal, otimizando a geração de insights para o desenvolvimento do relatório.

Para atender essa demanda, foi realizado os passos semelhantes aos realizados na camada Silver:

        Exploração dos Dados na Camada Silver: Iniciamos o processo exploratório dos dados contidos na camada Silver.

        Criação de um Script de Transformação de Dados: Desenvolvemos um script dedicado à transformação dos dados, visando aprimorar a qualidade e relevância das informações.

        Integração da Nova Etapa no Pipeline de Dados: Adicionamos com sucesso essa nova etapa ao nosso pipeline de dados, assegurando a fluidez e eficácia do processo de transformação e análise.


## 📄Desenvolvimento de Competências:
|Atividades|Realizadas |
|----------|-----------|
| Compreender como funciona a arquitetura de medalhas | Explorar dados utilizando o PySpark
| Transformar dados utilizando o PySpark | Extrair dados utilizando o PySpark
| Salvar dados utilizando o PySpark | Executar scripts utilizando o SparkSubmit
| Instalar o modulo Spark | Utilizar o SparkSubmitOperator
| Atualizar uma DAG | Salvar os dados transformados pelo Spark
| Centralizar nossas pastas em um variável | Estruturar nosso data lake
| Reestruturar nosso código | Refinar informações para a camada Gold
| Utilizar um operador para transformar dados da camada Gold | Atualizar a DAG com a nova etapa de transformação
| Explorar os dados da camada Gold | |

## 🗂️Organização dos Arquivos
- Dados_transformation: Gravação de dados na etapa
- Datalake: Repositório Data Lake com arquitetura de medalhões - Camadas: Bronze, Silver e Gold, proporcionando maior organização ao Data Lake
- Hook: Implementação de um Hook no Airflow para realizar a conexão com a API utilizando o HTTP Hook. Esse Hook é utilizado para efetuar as requisições, utilizando a configuração de uma conexão no Airflow
- Operators: Desenvolvimento de um operador para extrair dados da API, criando um Data Lake e armazenando os dados nesse repositório
- Spark-3.1.3: Contém a distribuição binária do Apache Spark na versão 3.1.3, essa pasta é crucial para garantir que o ambiente Spark esteja corretamente configurado em seu sistema
 - SRC: Armazena o código fonte do projeto | Subpastas:
	Notebooks: Notebooks Jupyter, que contêm códigos, gráficos e comentários relacionados à análise e exploração de dados. Os Notebooks Jupyter são usados para executar código de forma interativa e são populares no ambiente de ciência de dados.
	Scripts: código que realiza a extração de dados de uma API.
	Spark: Scripts Python que utiliza o Apache Spark para realizar transformações, limpeza, manipulção e agregação de dados usando a capacidade de processamento distribuído do Spark
- DAGs: Automação do pipeline realizada por meio do DAG, no qual são especificadas as instruções para o Airflow sobre como a extração do operador será executada. Define-se parâmetros como frequência, data inicial e data final.

## 🎞️Imagens do Projeto

###### Imagem 3: Interface Airflow - Visualização DAG e sua execução
<img src="/assets/img/img-execucao-dag.png">

###### Imagem 4: Visualização gráfica de um DAG e suas dependências
<img src="/assets/img/img-grafico-dag.png">

###### Imagem 5: Visualização do calendário
<img src="/assets/img/img-calendario-dag.png">


## 🔍Referências
- [Alura](https://www.alura.com.br/)
