from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python_operator import PythonOperator
import os, tempfile
from airflow.models.xcom_arg import XComArg

# Replace the following path with the path to your mongo-spark-connector JAR file
mongo_spark_connector_jar = "/opt/spark/jars/mongodb-driver-sync-4.4.3.jar"

def receive_file_content(**kwargs):
    file_content = kwargs['dag_run'].conf['file_content']
    kwargs['ti'].xcom_push(key='file_content', value=file_content)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2023, 1, 1),
}

dag = DAG(
    dag_id="spark_cd_to_lpg",
    default_args=default_args,
    description="An Automated Patterns-based Model-to-Model Mapping and Transformation System for Labeled Property Graphs",
    schedule_interval=timedelta(days=1),
    catchup=False,
    max_active_runs=1,
)

t0 = PythonOperator(
    task_id='receive_file_content',
    python_callable=receive_file_content,
    provide_context=True,
    dag=dag
)

t1 = SparkSubmitOperator(
    task_id="Patterns_Processing",
    application="./applications/spark_patterns_processing_job.py",
    name="spark_patterns_processing_job",
    conf={'spark.jars.packages': 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,org.mongodb:mongodb-driver-sync:4.4.1'},
    application_args=["--run-id", "{{ run_id }}", "--file-content", "{{ ti.xcom_pull(task_ids='receive_file_content', key='file_content') }}"],
    dag=dag
)


# t2 = SparkSubmitOperator(
#     task_id="Graphs_Processing",
#     application="./applications/spark_graphs_processing_job.py",
#     name="spark_graphs_processing_job",
#     conf={'spark.jars.packages': 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,org.mongodb:mongodb-driver-sync:4.4.1'},
#     application_args=["--run-id", "{{ run_id }}"],
#     dag=dag
# )

t0 >> t1