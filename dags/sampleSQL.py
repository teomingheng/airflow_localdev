from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago




default_args = {
    'owner': 'Mingheng',
    'dag_id': 'Postgres_SQL_call',
    'start_date': days_ago(1),
    'schedule_interval': '@daily'
}

dag: DAG = DAG(
    dag_id='Postgres_SQL_call',
    default_args=default_args,
    template_searchpath='/opt/airflow/'
)

task1 = PostgresOperator(
    task_id="create_table",
    postgres_conn_id="POSTGRESDB",
    sql="sql/sample.sql",
    database="airflow",
    dag=dag
)

task1

