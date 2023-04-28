from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

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
    dag_id="spark_pi_estimation",
    default_args=default_args,
    description="Estimate Pi using Spark",
    schedule_interval=timedelta(days=1),
    catchup=False,
    max_active_runs=1,
)

t1 = SparkSubmitOperator(
    task_id="calculate_pi_estimate",
    application="./applications/spark_pi_estimation_job.py",
    name="spark_pi_estimation_job",
    dag=dag
)