"""
This module intends to process streaming data using spark
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

# Create connection

# spark = SparkSession.builder.appName("pyspark-labs-stream-processing").getOrCreate()
spark = SparkSession.builder\
    .master("spark://localhost:7077")\
    .appName("pyspark-labs-stream-processing")\
    .getOrCreate()

print(spark.version)
spark.range(5).show()


# Create DataFrame representing the stream of input lines from connection to localhost:9999
lines = spark.readStream.format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Split the lines into words
words = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("word")
)

# Generate running word count
wordCounts = words.groupBy("word").count()

# Start running the query that prints the running counts to the console
query = wordCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination() # prevent the process from exiting while the query is active

# start local data streaming using netcat `nc -lk 9999`
# only after this run the spark job otherwise it'll fail to listen on the port and fail to continue