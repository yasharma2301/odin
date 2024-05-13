from celery import Celery
import os
import urllib
import json
from app.utils.custom_logger import logger
from app.service.orchestrator_service.orchestrator import Orchestrator

orchestrator = Orchestrator()

aws_access_key_id=os.getenv('AWS_SERVER_PUBLIC_KEY')
aws_secret_access_key=os.getenv('AWS_SERVER_SECRET_KEY')
region_name=os.getenv('AWS_SERVER_REGION_KEY')
sqs_queue_url = "https://sqs.ap-south-1.amazonaws.com/975050081345/odin-main-queue"

BROKER_URL = 'sqs://{0}:{1}@'.format(
    urllib.parse.quote(aws_access_key_id, safe=''),
    urllib.parse.quote(aws_secret_access_key, safe='')
)

app = Celery(
    "app",
    broker_url=BROKER_URL,
    broker_transport_options={
        "region": region_name,
        "predefined_queues": {
            "celery": {
                "url": sqs_queue_url,
                "access_key_id": aws_access_key_id,
                "secret_access_key": aws_secret_access_key,
            }
        },
    },
    task_create_missing_queues=False,
)

@app.task
def process_message(message):
    parsed_message = json.loads(message)
    logger.info(f"Message body: {parsed_message}")

    orchestrator.run(parsed_message)