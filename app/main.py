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
from app.api.v1.file.file import router as file_router

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
app.include_router(file_router, prefix="/api/v1/file")
