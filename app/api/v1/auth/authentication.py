from fastapi import APIRouter
from app.models.auth.LoginRequest import LoginRequest
from fastapi.responses import JSONResponse
from app.service.AuthService import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/login")
async def login(login_request: LoginRequest):
    email, password = login_request.email, login_request.password

    try:
        res = auth_service.login(email, password)
        id_token = res.get('idToken')
        return JSONResponse(
            content={'token': id_token},
            status_code=400
        )
    except Exception as e:
        return JSONResponse(
            content={'error': f"ERROR: {str(e)}"},
            status_code=400
        )
    

@router.post("/signup")
async def login(signup_request: LoginRequest):
    email, password = signup_request.email, signup_request.password

    try:
        res = auth_service.signup(email, password)
        return JSONResponse(
            content={'message': f"Signed up successfully with user id: {res.uid}, you can now login!"},
            status_code=400
        )
    except Exception as e:
        return JSONResponse(
            content={'error': f"ERROR: {str(e)}"},
            status_code=400
        )