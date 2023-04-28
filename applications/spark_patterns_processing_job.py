from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
import os, random, copy, json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import argparse
# airflow id

from functions.find_np1_pattern import find_np1_pattern
from functions.find_np2_pattern import find_np2_pattern
from functions.find_np3_pattern import find_np3_pattern


from functions.find_cdp1_pattern import find_cdp1_pattern
from functions.find_cdp2_pattern import find_cdp2_pattern
from functions.find_cdp3_a_pattern import find_cdp3_a_pattern
from functions.find_cdp3_b_pattern import find_cdp3_b_pattern
from functions.find_cdp3_c_pattern import find_cdp3_c_pattern
from functions.find_cdp4_a_pattern import find_cdp4_a_pattern
from functions.find_cdp4_b_pattern import find_cdp4_b_pattern
from functions.find_cdp5_pattern import find_cdp5_pattern

from functions.find_sp1_pattern import find_sp1_pattern
from functions.find_sp2_a_pattern import find_sp2_a_pattern
from functions.find_sp2_b_pattern import find_sp2_b_pattern
from functions.find_sp3_a_pattern import find_sp3_a_pattern
from functions.find_sp3_b_pattern import find_sp3_b_pattern
from functions.find_sp3_c_pattern import find_sp3_c_pattern

from functions.find_gp1_a_pattern import find_gp1_a_pattern
from functions.find_gp1_b_pattern import find_gp1_b_pattern
from functions.find_gp2_pattern import find_gp2_pattern
from functions.find_gp3_pattern import find_gp3_pattern

from functions.group_classes_by_attributes import group_classes_by_attributes
from functions.to_labeled_property_graph import to_labeled_property_graph

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", help="Airflow run ID", required=True)
    parser.add_argument("--file-content", help="File content")
    args = parser.parse_args()
    run_id = args.run_id
    class_diagram = args.file_content


    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("patterns_processing_job") \
        .getOrCreate()

    #XML here

    # Code here
    soup = BeautifulSoup(class_diagram, 'lxml-xml')
    final_patterns = {"pattern": "", "nodes": [], "edges": []}
    c1_classes, c2_classes, c3_classes, other_classes = group_classes_by_attributes(soup)
    grouped_classes = (c1_classes, c2_classes, c3_classes, other_classes)
    result_patterns = []

    # Iterate over grouped_classes and run patterns for each group
    for group in grouped_classes:
    
      cdp1_patterns = find_cdp1_pattern(group)
      cdp2_patterns = find_cdp2_pattern(group)
      cdp3_a_patterns = find_cdp3_a_pattern(group)
      cdp3_b_patterns = find_cdp3_b_pattern(group)
      cdp3_c_patterns = find_cdp3_c_pattern(group)
      cdp4_a_patterns = find_cdp4_a_pattern(group)
      cdp4_b_patterns = find_cdp4_b_pattern(group)
      cdp5_patterns = find_cdp5_pattern(group)

      #
      sp1_patterns = find_sp1_pattern(group)
      sp2_a_patterns = find_sp2_a_pattern(group)
      sp2_b_patterns = find_sp2_b_pattern(group)
      sp3_a_patterns = find_sp3_a_pattern(group)
      sp3_b_patterns = find_sp3_b_pattern(group)
      sp3_c_patterns = find_sp3_c_pattern(group)

      #
      gp1_a_patterns = find_gp1_a_pattern(group)
      gp1_b_patterns = find_gp1_b_pattern(group)
      gp2_patterns = find_gp2_pattern(group)
      gp3_patterns = find_gp3_pattern(group)


      if cdp1_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, cdp1_patterns)
      if cdp2_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, cdp2_patterns)
      if cdp3_a_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, cdp3_a_patterns)
      if cdp3_b_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, cdp3_b_patterns)
      if cdp3_c_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, cdp3_c_patterns)
      if cdp4_a_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, cdp4_a_patterns)
      if cdp4_b_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, cdp4_b_patterns)
      if cdp5_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, cdp5_patterns)

      if sp1_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, sp1_patterns)
      if sp2_a_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, sp2_a_patterns)
      if sp2_b_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, sp2_b_patterns)
      if sp3_a_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, sp3_a_patterns)
      if sp3_b_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, sp3_b_patterns)
      if sp3_c_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, sp3_c_patterns)

      #GP

      if gp2_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, gp2_patterns)
      if gp3_patterns:
          final_patterns = to_labeled_property_graph(final_patterns, gp3_patterns)

      # at the end because it will cause copys of data structure
      if gp1_a_patterns and gp1_b_patterns:
        final_patterns_a = copy.deepcopy(final_patterns)
        final_patterns_b = copy.deepcopy(final_patterns)
        #
        final_patterns_a = to_labeled_property_graph(final_patterns_a, gp1_a_patterns)
        final_patterns_b = to_labeled_property_graph(final_patterns_b, gp1_b_patterns)


    if(gp1_a_patterns or gp1_b_patterns):
      result_patterns = [final_patterns_a, final_patterns_b]
      #assessments = calculate_assessments(result_patterns)
    else:
      result_patterns = final_patterns
      #print(final_patterns,"final_patterns")
      #assessments = calculate_assessments(final_patterns)
    
    json_string = json.dumps(result_patterns)
    data_df = spark.createDataFrame([(json_string,)], ["final_patterns"])
    data_df = data_df.withColumn("run_id", lit(run_id))

    # write to mongo
    data_df.write \
    .format("mongo") \
    .mode("append") \
    .option("spark.mongodb.output.uri", "mongodb+srv://airflow:airflow@m2mcluster0.c7niu07.mongodb.net/M2M.lpgs?retryWrites=true&w=majority") \
    .save()

    

    # file_path = os.path.join('/home/airflow', 'output.xml')
    # with open(file_path, 'w') as xml_file:
    #     xml_file.write(str(cdp3_c_patterns))

    # Stop the SparkSession
    spark.stop()

if __name__ == "__main__":
    main()
