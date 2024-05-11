from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth.authentication import router as auth_login_router
from app.api.v1.repo.repository import router as repo_router
import firebase_admin
from firebase_admin import credentials

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

app.include_router(auth_login_router, prefix="/api/v1/auth")
app.include_router(repo_router, prefix="/api/v1/repository")
