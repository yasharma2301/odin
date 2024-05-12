import asyncio
import random
import sys
import os
import botocore.exceptions
from aiobotocore.session import get_session
from app.constants.constants import default_queue
from app.utils.custom_logger import logger

QUEUE_NAME = default_queue

aws_access_key_id = os.getenv('AWS_SERVER_PUBLIC_KEY')
aws_secret_access_key = os.getenv('AWS_SERVER_SECRET_KEY')
region_name = os.getenv('AWS_SERVER_REGION_KEY')


async def queue_message(message_body):
    session = get_session()
    async with session.create_client(service_name='sqs', region_name=region_name,
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key) as client:
        try:
            response = await client.get_queue_url(QueueName=QUEUE_NAME)
        except botocore.exceptions.ClientError as err:
            if (
                err.response['Error']['Code']
                == 'AWS.SimpleQueueService.NonExistentQueue'
            ):
                logger.error(f"Queue {QUEUE_NAME} does not exist")
                sys.exit(1)
            else:
                raise

        queue_url = response['QueueUrl']

        logger.info('Putting messages on the queue')

        msg_no = 1
        while True:
            try:
                await client.send_message(
                    QueueUrl=queue_url, MessageBody=message_body
                )
                msg_no += 1

                logger.info(f'Pushed "{message_body}" to queue')

                await asyncio.sleep(random.randint(1, 4))
            except KeyboardInterrupt:
                break

        logger.info('Finished')


async def read_message(callback):
    session = get_session()
    async with session.create_client(service_name='sqs', region_name=region_name,
                                     aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key) as client:
        try:
            response = await client.get_queue_url(QueueName=QUEUE_NAME)
        except botocore.exceptions.ClientError as err:
            if (
                err.response['Error']['Code']
                == 'AWS.SimpleQueueService.NonExistentQueue'
            ):
                logger.info(f"Queue {QUEUE_NAME} does not exist")
                sys.exit(1)
            else:
                raise

        queue_url = response['QueueUrl']

        logger.info('Pulling messages off the queue')

        while True:
            try:
                # This loop won't spin really fast as there is
                # essentially a sleep in the receive_message call
                response = await client.receive_message(
                    QueueUrl=queue_url,
                    WaitTimeSeconds=2,
                )

                if 'Messages' in response:
                    for msg in response['Messages']:
                        logger.info(f'Got msg "{msg["Body"]}"')

                        await callback(msg['Body'])

                        await client.delete_message(
                            QueueUrl=queue_url,
                            ReceiptHandle=msg['ReceiptHandle'],
                        )
                else:
                    logger.info('No messages in queue')
            except KeyboardInterrupt:
                break

        logger.info('Finished')


# loop = asyncio.get_event_loop()
# loop.run_until_complete(queue_message())
