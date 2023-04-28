from pyspark.sql import SparkSession
import random

def calculate_pi(n):
    inside_circle = 0

    for _ in range(n):
        x = random.random()
        y = random.random()
        distance = x**2 + y**2

        if distance <= 1:
            inside_circle += 1

    return inside_circle

def main():
    # Initialize SparkSession
    spark = SparkSession.builder \
        .appName("High Parallelism Performance Test2") \
        .getOrCreate()

    num_samples = 1000000000
    num_tasks = 100000

    samples_per_task = num_samples // num_tasks

    # Create an RDD with num_tasks partitions
    rdd = spark.sparkContext.parallelize(range(num_tasks), num_tasks)

    # Calculate the value of Pi using Monte Carlo method
    inside_circle_counts = rdd.map(lambda _: calculate_pi(samples_per_task)).collect()

    total_inside_circle = sum(inside_circle_counts)
    pi_estimate = 4.0 * total_inside_circle / num_samples

    print("Pi estimate:", pi_estimate)

    # Stop the SparkSession
    spark.stop()

if __name__ == "__main__":
    main()
