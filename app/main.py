from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth.authentication import router as auth_login_router
from app.api.v1.repo.repository import router as repo_router
import firebase_admin
from firebase_admin import credentials
from app.core.setup_sql import Base, database_engine
# Do not remove - Required for creating tables | TODO: Find a better way to do this
from app.models.entity import user, repository, metadata, file
import asyncio
from app.service.queue_service.async_queue_service import read_message
from app.listeners.repo_queue_listener import process_message

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

# Async tasks
# asyncio.run(read_message(process_message))

if __name__ == 'app.main':
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    if loop and loop.is_running():
        print('Async event loop already running. Adding coroutine to the event loop.')
        tsk = loop.create_task(read_message(process_message))
        tsk.add_done_callback(
            lambda t: print(f'Task done with result={t.result()}  << return val of main()'))
    else:
        print('Starting new event loop')
        result = asyncio.run(read_message(process_message))