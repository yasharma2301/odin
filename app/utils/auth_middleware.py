from fastapi.requests import Request
from app.service.auth_service.auth_service import AuthService
from fastapi import HTTPException


class AuthMiddleware:
    @classmethod
    async def check_auth(cls, request: Request):

        log_prefix = "AuthMiddleware::__call__:"
        try:
            headers = request.headers
            bearer_auth = headers.get('authorization')
            auth_tokens = bearer_auth.split(' ')
            assert auth_tokens[0] == 'Bearer'
            jwt = auth_tokens[1]
            user_id = AuthService.check_auth(jwt)
            request.state.user_id = user_id
        except Exception as e:
            print(f"{log_prefix} {str(e)}")
            raise HTTPException(status_code=403, detail="Unauthorized")

