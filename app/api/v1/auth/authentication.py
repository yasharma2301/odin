from fastapi import APIRouter, Depends
from app.models.dto.auth.LoginRequest import LoginRequest
from fastapi.responses import JSONResponse
from app.service.auth_service.auth_service import AuthService
from app.core.setup_sql import get_db
from app.models.dto.auth.SignupRequest import SignupRequest
from app.repository.user_repo.user_rep import UserRepo

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
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={'error': f"ERROR: {str(e)}"},
            status_code=400
        )
    

@router.post("/signup")
async def login(signup_request: SignupRequest, db=Depends(get_db)):
    email, password, name = signup_request.email, signup_request.password, signup_request.full_name

    try:
        res = auth_service.signup(email, password, name)
        user_base = {'email': email, 'name': name, 'uid': res.uid}
        user_repository = UserRepo()
        created_user = user_repository.create_user(user_base)
        return JSONResponse(
            content=created_user.to_json(),
            status_code=201
        )
    except Exception as e:
        return JSONResponse(
            content={'error': f"ERROR: {str(e)}"},
            status_code=400
        )
