from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.service.repository_service.repository_service import RepositoryService
from app.service.AuthService import AuthService
from app.models.repository.repository import RepositoryProcessRequest
from app.utils.auth_middleware import AuthMiddleware
from app.utils.general import get_current_user, current_milli_time
from fastapi.requests import Request
from app.service.parser_service.parser_service import CodeParserService

router = APIRouter()
repository_service = RepositoryService()
auth_service = AuthService()
code_parser_service = CodeParserService()


@router.post("/process", dependencies=[Depends(AuthMiddleware.check_auth)])
async def process(request: Request, repository_request: RepositoryProcessRequest):

    try:
        url = repository_request.url
        folder_name = f"{get_current_user(request)}-{current_milli_time()}"
        repository_service.clone_local(url, folder_name)
        return JSONResponse(
            content={'status': "SUCCESS"},
            status_code=200
        )
    except Exception as e:
        return JSONResponse(
            content={
                'status': 'ERROR',
                'message': str(e)
            },
            status_code=400
        )


@router.post("/dumb")
async def dumb(request: Request):
    return repository_service.walk_repository_and_collect_results()
    # return code_parser_service.parse_file()
