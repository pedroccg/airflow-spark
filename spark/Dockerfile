FROM bitnami/spark:3.3.0
USER root
RUN apt-get update && \
    apt-get install -y curl && \
    curl -o /opt/bitnami/spark/jars/mongodb-driver-sync-4.8.0.jar "https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-sync/4.8.0/mongodb-driver-sync-4.8.0.jar"