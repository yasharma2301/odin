from app.utils.custom_logger import logger
import asyncio
import aioboto3


async def receive_messages(queue_url, max_number, wait_time):
    """
    Receive a batch of messages asynchronously in a single request from an SQS queue.

    :param queue_url: The URL of the queue from which to receive messages.
    :param max_number: The maximum number of messages to receive. The actual number
                       of messages received might be less.
    :param wait_time: The maximum time to wait (in seconds) before returning. When
                      this number is greater than zero, long polling is used. This
                      can result in reduced costs and fewer false empty responses.
    :return: The list of Message objects received. These each contain the body
             of the message and metadata and custom attributes.
    """
    async with aioboto3.client('sqs') as sqs:
        try:
            response = await sqs.receive_message(
                QueueUrl=queue_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=max_number,
                WaitTimeSeconds=wait_time
            )
            messages = response.get('Messages', [])
            for msg in messages:
                logger.info("Received message: %s: %s", msg['MessageId'], msg['Body'])
            return messages
        except Exception as error:
            logger.exception("Couldn't receive messages from queue: %s", queue_url)
            raise error


async def listen_for_messages(queue_url, max_number, wait_time):
    while True:
        messages = await receive_messages(queue_url, max_number, wait_time)
        if messages:
            await process_messages(messages)


async def process_messages(messages):
    logger.info("Processing %s messages", len(messages))
    await asyncio.sleep(5)




