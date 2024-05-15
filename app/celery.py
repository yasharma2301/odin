from celery import Celery, Task
import os
import urllib


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
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    worker_concurrency=1,
    celery_routes = {
        'tasks.celery.run_process':{
            'queue' : 'odin-main-queue'
        }
    }
)

@app.task(name="celery.run_process", bind=True)
def run_process():
    print("Message received")
    return "Task executed successfully"


# celery --app=app.celery worker --pool=solo --concurrency=1 --loglevel=DEBUG --queues=celery -E