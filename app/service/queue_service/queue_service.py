import boto3
from app.utils.custom_logger import logger
from botocore.exceptions import ClientError
import os

session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_SERVER_PUBLIC_KEY'),
    aws_secret_access_key=os.getenv('AWS_SERVER_SECRET_KEY'),
    region_name=os.getenv('AWS_SERVER_REGION_KEY'),
)
sqs = session.resource("sqs")


class QueueService:
    def get_queue(self, name):
        """
        Gets an SQS queue by name.

        :param name: The name that was used to create the queue.
        :return: A Queue object.
        """
        try:
            queue = sqs.get_queue_by_name(QueueName=name)
            logger.info("Got queue '%s' with URL=%s", name, queue.url)
        except ClientError as error:
            logger.exception("Couldn't get queue named %s.", name)
            raise error
        else:
            return queue

    def send_message(self, queue, message_body, message_group_id, message_attributes=None):
        """
        Send a message to an Amazon SQS queue.

        :param queue: The queue that receives the message.
        :param message_body: The body text of the message.
        :param message_attributes: Custom attributes of the message. These are key-value
                                   pairs that can be whatever you want.
        :return: The response from SQS that contains the assigned message ID.
        """
        if not message_attributes:
            message_attributes = {}

        try:
            response = queue.send_message(
                MessageBody=message_body, MessageAttributes=message_attributes, MessageGroupId=message_group_id
            )
        except ClientError as error:
            logger.exception("Send message failed: %s", message_body)
            raise error
        else:
            return response

    def receive_messages(self, queue, max_number, wait_time):
        """
        Receive a batch of messages in a single request from an SQS queue.

        :param queue: The queue from which to receive messages.
        :param max_number: The maximum number of messages to receive. The actual number
                           of messages received might be less.
        :param wait_time: The maximum time to wait (in seconds) before returning. When
                          this number is greater than zero, long polling is used. This
                          can result in reduced costs and fewer false empty responses.
        :return: The list of Message objects received. These each contain the body
                 of the message and metadata and custom attributes.
        """
        try:
            messages = queue.receive_messages(
                MessageAttributeNames=["All"],
                MaxNumberOfMessages=max_number,
                WaitTimeSeconds=wait_time,
            )
            for msg in messages:
                logger.info("Received message: %s: %s", msg.message_id, msg.body)
        except ClientError as error:
            logger.exception("Couldn't receive messages from queue: %s", queue)
            raise error
        else:
            return messages
