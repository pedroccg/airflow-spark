# Dockerfile-webserver
FROM apache/airflow:2.5.3-python3.8

USER root
# Download and extract Spark binary distribution
ARG SPARK_VERSION=3.3.0
ARG HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark

RUN curl -fsSL https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz | tar xz -C /opt && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} $SPARK_HOME

# Set environment variables for JAVA_HOME and SPARK_HOME
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Install Java
USER root
RUN apt-get update \
    && apt-get install -y openjdk-11-jdk-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow
RUN pip install --no-cache-dir --user apache-airflow-providers-apache-spark pyspark==3.3.0 pandas

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

USER root
COPY airflow.cfg /opt/airflow/airflow.cfg
RUN chown airflow: /opt/airflow/airflow.cfg

# Copy spark-defaults.conf file if needed
COPY spark-defaults.conf $SPARK_HOME/conf/
USER airflow