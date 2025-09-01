
# Weather Forecast DAG

Este proyecto contiene un DAG de Airflow para la ingesta y almacenamiento de datos meteorológicos desde la API pública de CONAGUA en Snowflake.

## Descripción

El DAG `weather_forecast_dag` realiza las siguientes tareas:

1. Inicializa la base de datos y el esquema en Snowflake usando el script `init_db.sql`.
2. Obtiene datos meteorológicos desde la API [CONAGUA](https://smn.conagua.gob.mx/tools/GUI/webservices/index.php?method=3), los procesa y los almacena en la tabla `CONAGUA_WEATHER_RAW` en Snowflake.
3. Limpia la tabla usando el script `limpiar.sql`.

La lógica de ingesta y carga está implementada en `include/weather_api.py`.

## Estructura del DAG

- **dags/weather_forecast_dag.py**: Define el flujo de trabajo y las tareas principales.
- **include/weather_api.py**: Contiene la clase y funciones para consumir la API, transformar los datos y cargarlos en Snowflake.
- **include/init_db.sql**: Script para inicializar la tabla en Snowflake.
- **include/limpiar.sql**: Script para limpiar la tabla.

## Configuración

Antes de ejecutar el DAG, asegúrate de:

- Configurar la conexión a Snowflake en Airflow (`snowflake_conn_id_jr`).
- Modificar los parámetros de base de datos, esquema y tabla si es necesario en el DAG.
- Instalar los paquetes requeridos en `requirements.txt`.

## Ejecución

Para ejecutar el DAG localmente:

1. Inicia Airflow con Docker:
    ```bash
    astro dev start
    ```
2. Accede a la UI de Airflow en [http://localhost:8080/](http://localhost:8080/).
3. Activa el DAG `weather_forecast_dag` y verifica la ejecución de las tareas.

## Personalización

Puedes modificar la frecuencia de ejecución del DAG cambiando el parámetro `schedule` en el decorador `@dag`.

## Referencias

- [Documentación Airflow](https://airflow.apache.org/)
- [Documentación Snowflake](https://docs.snowflake.com/)

Contact
=======

The Astronomer CLI is maintained with love by the Astronomer team. To report a bug or suggest a change, reach out to our support.
