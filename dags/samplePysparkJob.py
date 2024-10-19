import pendulum

from airflow.models import DAG
from airflow.utils.dates import days_ago

# Import SparkSession
from pyspark.sql import SparkSession


DEFAULT_ARGS = {
    'owner': 'Mingheng',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'catchup': False,
}


with DAG(
    default_args=DEFAULT_ARGS,
    dag_id="PySparkJob",
    template_searchpath='/opt/airflow/',
    schedule=None,
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["pyspark"]
    ) as dag:

    @dag.task
    def sparkJob():
      """
      Create spark session, read file from source, returns a spark df
      """

      # Create SparkSession 
      spark = (SparkSession.builder
              .master("local[1]")
              .appName("Spark")
              .getOrCreate() 
              )
      
      # Read the source file
      df = spark.read.csv("./data/source/annual-enterprise-survey-2023-financial-year-provisional-size-bands.csv", header=True)
      df.printSchema()
      df.show()

      # Write to target dir and convert to parquet format
      now = pendulum.now()
      df.write.parquet(f"./data/target/sampleData-{now}") 

      # success
      print('job done')
      
      return


    sparkJob_run = sparkJob()
    sparkJob_run
