from datetime import datetime, timezone
from random import randint

from faker import Faker
from pyspark.sql import Row, SparkSession

# Create connection

spark = SparkSession.builder.appName("pyspark-labs").getOrCreate()

print(spark.version)
spark.range(5).show()


# Generate dataframe

def generate_user_data(n):
    """Generate and return user data one at a time."""
    fake = Faker()
    for _ in range(n):
        yield {
            "name": fake.name(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "job": fake.job(),
            "date_of_birth": fake.date_of_birth(),
            "company": fake.company(),
            "address": fake.address(),
            "ssn": fake.ssn(),
            "state": fake.state(),
            "country": fake.country(),
            "salary": randint(50_000, 200_000)
        }

n = 100
df = spark.createDataFrame([
    Row(name=user["name"],
        email=user["email"],
        phone_number=user["phone_number"],
        job=user["job"],
        date_of_birth=user["date_of_birth"],
        company=user["company"],
        address=user["address"],
        ssn=user["ssn"],
        state=user["state"],
        country=user["country"],
        salary=user["salary"]
    )
    for user in generate_user_data(n)
])
df.show()

# Write to s3
# same for parquet, csv and orc formats
timestamp = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M")
# file_path = f's3a://pyspark-labs/user-data-{timestamp}.csv'
# file_path = f's3a://pyspark-labs/user-data-{timestamp}.parquet'
file_path = f's3a://pyspark-labs/user-data-{timestamp}.orc'

print("***************************************************")
print("Writing data to S3...")
print("***************************************************")

# df.write.csv(file_path, header=True, mode='overwrite')
# df.write.parquet(file_path, mode='overwrite')
df.write.orc(file_path, mode='overwrite')
print("***************************************************")
print("Writing data to S3 complete...")
print("***************************************************")



# Read data from s3

print("***************************************************")
print("Reading from S3...")
print("***************************************************")

# rdf = spark.read.csv(file_path, header=True, multiLine=True, escape='"')
# rdf = spark.read.parquet(file_path)
rdf = spark.read.orc(file_path)
rdf.show()

print("***************************************************")
print("Reading from S3 complete...")
print("***************************************************")

# spark.stop()
