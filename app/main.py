from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth.authentication import router as auth_login_router
from app.api.v1.repo.repository import router as repo_router
import firebase_admin
from firebase_admin import credentials
from app.core.setup_sql import Base, database_engine
# Do not remove - Required for creating tables | TODO: Find a better way to do this
from app.models.entity import user, repository, metadata, file
from app.listeners.repo_queue_listener import listen_for_messages
import asyncio
from app.service.queue_service.queue_service import QueueService
from app.constants.constants import default_queue


# Initialize FastAPI app
app = FastAPI(
    description="The odin project",
    title="Odin",
    docs_url="/"
)

# Configure CORS
# Setting * as value for now as this is not a production level server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("./odin-firebase-service-account.json")
    firebase_admin.initialize_app(cred)

# Initialize Mysql
Base.metadata.create_all(bind=database_engine)

# Api routes configuration
app.include_router(auth_login_router, prefix="/api/v1/auth")
app.include_router(repo_router, prefix="/api/v1/repository")


if __name__ == "app.main":
    queue_service = QueueService()
    odin_queue = queue_service.get_queue(default_queue)

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # 'RuntimeError: There is no current event loop...'
        loop = None

    if loop and loop.is_running():
        print('Async event loop already running. Adding coroutine to the event loop.')
        tsk = loop.create_task(listen_for_messages(odin_queue.url, 10, 20))
        # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
        # Optionally, a callback function can be executed when the coroutine completes
        tsk.add_done_callback(
            lambda t: print(f'Task done with result={t.result()}  << return val of main()'))
    else:
        print('Starting new event loop')
        result = asyncio.run(listen_for_messages(odin_queue.url, 10, 20))
