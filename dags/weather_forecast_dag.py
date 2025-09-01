import os
from datetime import datetime
from airflow import DAG
from airflow.decorators import dag, task
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from include.weather_api import run_weather_forecast_pipeline
from airflow.models import Variable

# Definimos las configuraciones básicas para la ejecución
URL = "https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=3"
SNOWFLAKE_CONN_ID = "snowflake_conn_id_jr"  # ID de conexión configurado en Airflow
DATABASE = "JHONATTAN_ICESI"  # Nombre de la base de datos en Snowflake
SCHEMA = "JHONATTAN_ICESI"  # Nombre del esquema en Snowflake
TABLE = "CONAGUA_WEATHER_RAW"  # Nombre de la tabla de destino en Snowflake


# Definimos el DAG usando el decorador @dag de Airflow
@dag(
    schedule="*/20 * * * *",  # Configuramos el DAG para que se ejecute todos los días
    start_date=datetime(2025, 8, 31),  # Se iniciará desde el día anterior para pruebas
    catchup=False,  # Evitamos la ejecución de tareas atrasadas
    default_args={"owner": "Jhonattan", "retries": 2},
    tags=["weather", "snowflake"],  # Etiquetas para categorizar el DAG en Airflow
    template_searchpath="/usr/local/airflow/include",  # Carpeta donde Airflow busca archivos SQL
)
def weather_forecast_dag():

    # Tarea principal que obtiene los datos de clima y los guarda en Snowflake
    @task()
    def fetch_and_save_weather_data():
        # Ejecutamos el pipeline para obtener los datos del clima y guardarlos en Snowflake
        run_weather_forecast_pipeline(
            url=URL,
            snowflake_conn_id=SNOWFLAKE_CONN_ID,
            database=DATABASE,
            schema=SCHEMA,
            table=TABLE,
        )

    init_db = SnowflakeOperator(
        task_id="init_db",
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
        sql="init_db.sql",
        params={"database": DATABASE, "schema": SCHEMA},
    )

    clean_data = SnowflakeOperator(
        task_id="clean_data",
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
        sql="limpiar.sql",
        params={"database": DATABASE, "schema": SCHEMA},
    )

    # Establecemos el flujo de tareas
    # Primero cargamos los datos, luego inicializamos la BD y finalmente limpiamos
    init_db >> fetch_and_save_weather_data() >> clean_data


# Instanciamos el DAG
dag = weather_forecast_dag()
