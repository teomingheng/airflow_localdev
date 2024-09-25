import os
import pendulum
import requests 
import polars as pl

from datetime import timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.postgres.operators.postgres import PostgresOperator


POSTGRES_DB = os.environ.get("AIRFLOW_CONN_POSTGRESDB")
print("POSTGRES_DB %s", POSTGRES_DB)

API_ENDPOINT = "https://health.data.ny.gov/resource/keti-qx5t.json?$limit=50"
DEFAULT_ARGS = {
    'owner': 'Mingheng',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
  
}


with DAG(
    default_args=DEFAULT_ARGS,
    dag_id="API_to_DB_DAG",
    template_searchpath='/opt/airflow/',
    schedule=None,
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["externalAPI_to_DB"]
    ) as dag:

    # 1st DAG to setup a new DB schema and create the table
    setup_medicaid_schema = PostgresOperator(
        task_id="setup_medicaid_schema",
        postgres_conn_id='POSTGRESDB',
        sql="sql/medicaid_db_init.sql",
        database="airflow"
    )

    @dag.task
    def get_json_data():
      """
      This function is used to get the json data from the NY Health API (medicaid providers).
      """
      # Call external Api to get data
      result = requests.get(API_ENDPOINT)
      if result.status_code == 200:
          print("Call to api successful")
          if not result.json():
              raise ValueError(
                  "No Data fetched from API")
          # Getting response in json
          json_data = result.json()
      else:
          print("Error in Api Call")

      return json_data

    @dag.task
    def transform_and_load_data(json_data):

        # Load json data into df
        df = pl.DataFrame((json_data))
        print(df.head(2))

        # Fix data type
        df = df.with_columns(
            pl.col("enrollment_begin_date").str.to_datetime()
            ,pl.col("next_anticipated_revalidation_date").str.to_datetime()
            ,pl.col("updated").str.to_datetime()
        )
    
        # Rename column
        df = df.rename({"state": "us_state"})
    
        # write to DB 
        df.write_database(
            table_name="medicaid.listing",
            connection=POSTGRES_DB,
            if_table_exists="append",
        )  

        return


    get_data = get_json_data()
    transform_and_load = transform_and_load_data(get_data)

    setup_medicaid_schema >> get_data >> transform_and_load