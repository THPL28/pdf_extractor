from fastapi import FastAPI, UploadFile, HTTPException, Form
import boto3
from kafka import KafkaProducer
import json
import uuid
import os
import logging
from prometheus_fastapi_instrumentator import Instrumentator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PDF Ingestion Service")
Instrumentator().instrument(app).expose(app)

# Configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "pdf-extraction-jobs")
S3_BUCKET = os.getenv("S3_BUCKET", "pdf-processor-raw")
S3_ENDPOINT = os.getenv("S3_ENDPOINT")

s3_client = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.post("/upload", status_code=202)
async def upload_pdf(
    file: UploadFile, 
    intelligent: bool = Form(False)  # New intelligent flag
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type.")
    
    try:
        content = await file.read()
        job_id = str(uuid.uuid4())
        s3_key = f"raw/{job_id}.pdf"
        
        s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=content)
        
        # We send the preference to Kafka
        message = {
            "job_id": job_id, 
            "s3_path": s3_key, 
            "original_filename": file.filename,
            "mode": "intelligent" if intelligent else "standard"
        }
        
        producer.send(KAFKA_TOPIC, key=job_id.encode('utf-8'), value=message)
        
        return {"job_id": job_id, "status": "processing", "mode": message["mode"]}
    except Exception as e:
        logger.error(f"Failed to ingest document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
