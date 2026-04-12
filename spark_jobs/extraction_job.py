from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, from_json
from pyspark.sql.types import StringType, StructType, StructField
import os

# Updated Schema with 'mode'
schema = StructType([
    StructField("job_id", StringType()),
    StructField("s3_path", StringType()),
    StructField("original_filename", StringType()),
    StructField("mode", StringType())
])

def process_pdf_partition(s3_path, mode="standard"):
    import boto3
    from infrastructure.factories.extraction_factory import ExtractionFactory
    
    s3 = boto3.client(
        's3',
        endpoint_url=os.getenv("S3_ENDPOINT", "http://minio:9000"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "minioadmin"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin"),
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )
    bucket = os.getenv("S3_BUCKET", "pdf-processor-raw")
    
    try:
        response = s3.get_object(Bucket=bucket, Key=s3_path)
        file_bytes = response['Body'].read()
        
        # Branching logic based on user preference
        if mode == "intelligent":
            return ExtractionFactory.extract_intelligent(file_bytes)
        else:
            return ExtractionFactory.extract_with_fallback(file_bytes)
            
    except Exception as e:
        return f"ERROR: {str(e)}"

process_pdf_udf = udf(process_pdf_partition, StringType())

def main():
    spark = SparkSession.builder.appName("PDF-Extractor-Dynamic").getOrCreate()

    kafka_options = {
        "kafka.bootstrap.servers": os.getenv("KAFKA_SERVERS", "kafka:9092"),
        "subscribe": os.getenv("KAFKA_TOPIC", "pdf-extraction-jobs"),
        "startingOffsets": "earliest"
    }

    raw_df = spark.readStream.format("kafka").options(**kafka_options).load()
    parsed_df = raw_df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
    
    # Passing both s3_path and mode to the UDF
    results_df = parsed_df.withColumn(
        "extracted_text", 
        process_pdf_udf(col("s3_path"), col("mode"))
    )

    query = results_df.writeStream.outputMode("append").format("console").option("truncate", "false").start()
    query.awaitTermination()

if __name__ == "__main__":
    main()
