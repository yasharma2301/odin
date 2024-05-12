import json
from app.utils.custom_logger import logger
from app.service.queue_service.queue_service import QueueService
from app.service.orchestrator_service.orchestrator import Orchestrator


queue_service = QueueService()
orchestrator = Orchestrator()


async def listen_for_messages(odin_queue, max_number, wait_time):
    while True:
        messages = queue_service.receive_messages(odin_queue, max_number, wait_time)
        for message in messages:
            await process_message(message)


async def process_message(message):
    body, message_id = message.body, message.message_id
    logger.info(f"Processing message with id: {message_id}")

    parsed_body = json.loads(body)
    logger.info(f"Message body: {parsed_body}")

    orchestrator.run(parsed_body)

    # Delete record after consuming
    queue_service.delete_message(message)
