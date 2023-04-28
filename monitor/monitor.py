import time
import requests
from datetime import datetime, timedelta

def get_active_spark_sessions(spark_master_host, spark_master_port):
    url = f"http://{spark_master_host}:{spark_master_port}/v1/submissions/status"
    response = requests.get(url)
    data = response.json()

    active_sessions = []
    for app in data:
        app_id = app['id']
        app_start_time = app['startTimeEpoch']  # in milliseconds since epoch
        app_name = app['name']
        active_sessions.append((app_id, app_start_time, app_name))

    return active_sessions

def terminate_idle_sessions(spark_master_host, spark_master_port, idle_time_threshold):
    active_sessions = get_active_spark_sessions(spark_master_host, spark_master_port)
    current_time = datetime.now()

    for app_id, app_start_time, app_name in active_sessions:
        app_start_datetime = datetime.fromtimestamp(app_start_time / 1000)
        idle_time = current_time - app_start_datetime

        if idle_time > idle_time_threshold:
            # Terminate the idle session
            print(f"Terminating idle session: {app_id}, {app_name}")
            # Add your logic to terminate the session, e.g., using YARN API or Kubernetes API

# Main monitoring loop
spark_master_host = "master"
spark_master_port = "6066"
idle_time_threshold = timedelta(minutes=10)

while True:
    terminate_idle_sessions(spark_master_host, spark_master_port, idle_time_threshold)
    time.sleep(60)  # Check for idle sessions every 60 seconds