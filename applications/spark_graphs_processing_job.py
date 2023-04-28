from pyspark.sql import SparkSession
import random
import argparse
from pyspark.sql.functions import lit
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, MapType
import pandas as pd
from pyspark.sql import functions as F
import json


# airflow id
parser = argparse.ArgumentParser()
parser.add_argument("--run-id", help="Airflow run ID", required=True)
args = parser.parse_args()
run_id = args.run_id


def to_labeled_property_graph(final_patterns, pattern_classes):
    nodes = []
    edges = []

    # Convert the pattern_classes DataFrame to a list of dictionaries
    pattern_classes_list = pattern_classes.select("*").toPandas().to_dict(orient="records")

    for class_element in pattern_classes_list:
        label = class_element['label']
        class_id = class_element['id']
        #properties = class_element['properties']
        properties = class_element.get('properties', [])


        nodes.append({"id": class_id, "label": label, "properties": properties})

        relations = class_element.get('relations', [])
        for relation in relations:
            source = relation['source']
            target = relation['target']
            value = relation['value']
            edge_id = relation['id']
            restriction = relation['restriction']
            edges.append({"id": edge_id, "source": source, "target": target, "value": value, "restriction": restriction})

    # graph = {
    #     "pattern": pattern_name,
    #     "nodes": nodes,
    #     "edges": edges
    # }

    #final_patterns["pattern"] = pattern_name

    # Append nodes if they don't already exist in final_patterns
    for node in nodes:
        if node not in final_patterns['nodes']:
            final_patterns['nodes'].append(node)

    # Append edges if they don't already exist in final_patterns
    for edge in edges:
        edge_id = edge['id']
        edge_id_reversed = "_".join(reversed(edge_id.split("_")))
        if not any(existing_edge['id'] in (edge_id, edge_id_reversed) for existing_edge in final_patterns['edges']):
            final_patterns['edges'].append(edge)

    return final_patterns


def main():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("graphs_processing_job") \
        .getOrCreate()
    

    patterns_to_process = [
    ("cdp1"),
    ("cdp2"),
    ("cdp3a"),
    ("cdp3b"),
    ("cdp3c"),
    ("cdp4a"),
    ("cdp4b"),
    ("cdp5"),
    ("sp1"),
    ("sp2a"),
    ("sp2b"),
    ("sp3a"),
    ("sp3b"),
    ("sp3c"),
    ("gp1a"),
    ("gp1b"),
    ("gp2"),
    ("gp3")]

    final_patterns = {"pattern": "", "nodes": [], "edges": []}

    for patterns in patterns_to_process:
        # Read data from MongoDB
        df = spark.read \
            .format("mongo") \
            .option("spark.mongodb.input.uri", f"mongodb+srv://airflow:airflow@m2mcluster0.c7niu07.mongodb.net/M2M.{patterns}?retryWrites=true&w=majority") \
            .load()

        # Check if the DataFrame has the 'run_id' column
        if 'run_id' in df.columns:
            # Filter data by run_id
            filtered_df = df.filter(df.run_id == run_id)  
            if not filtered_df.rdd.isEmpty():
                final_patterns = to_labeled_property_graph(final_patterns, filtered_df)
    
    json_string = json.dumps(final_patterns)
    data_df = spark.createDataFrame([(json_string,)], ["final_patterns"])
    data_df = data_df.withColumn("run_id", lit(run_id))


    # Filter data by run_id
    # filtered_df = df_cdp3c.filter(df_cdp3c.run_id == run_id)
    # final_patterns = {"pattern": "", "nodes": [], "edges": []}
    # final_patterns = to_labeled_property_graph(final_patterns, filtered_df)
    # json_string = json.dumps(final_patterns)
    # data_df = spark.createDataFrame([(json_string,)], ["final_patterns"])
    # data_df = data_df.withColumn("run_id", lit(run_id))

    # nodes_schema = StructType([
    #     StructField("id", StringType(), True),
    #     StructField("label", StringType(), True),
    #     StructField("properties", MapType(StringType(), StringType()), True)
    # ])
    # edges_schema = StructType([
    #     StructField("id", StringType(), True),
    #     StructField("source", StringType(), True),
    #     StructField("target", StringType(), True),
    #     StructField("value", StringType(), True),
    #     StructField("restriction", StringType(), True)
    # ])
    # nodes_data = [(node["id"], node["label"], node["properties"]) for node in final_patterns['nodes']]
    # edges_data = [(edge["id"], edge["source"], edge["target"], edge["value"], edge["restriction"]) for edge in final_patterns['edges']]
    # nodes_df = spark.createDataFrame(data=nodes_data, schema=nodes_schema)
    # edges_df = spark.createDataFrame(data=edges_data, schema=edges_schema)
    # c_df = spark.createDataFrame(c_dict)
    # c_df = c_df.withColumn("run_id", lit(run_id))

    data_df.write \
    .format("mongo") \
    .mode("append") \
    .option("spark.mongodb.output.uri", "mongodb+srv://airflow:airflow@m2mcluster0.c7niu07.mongodb.net/M2M.lpgs?retryWrites=true&w=majority") \
    .save()


    # Stop the SparkSession
    spark.stop()

if __name__ == "__main__":
    main()
