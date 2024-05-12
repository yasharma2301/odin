import json
from app.utils.custom_logger import logger
from app.service.orchestrator_service.orchestrator import Orchestrator

orchestrator = Orchestrator()


async def process_message(message):
    parsed_message = json.loads(message)
    logger.info(f"Message body: {parsed_message}")

    orchestrator.run(parsed_message)
