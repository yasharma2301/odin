import json
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.service.repository_service.repository_service import RepositoryService
from app.service.auth_service.auth_service import AuthService
from app.models.dto.repository.repository import RepositoryProcessRequest
from app.utils.auth_middleware import AuthMiddleware
from app.utils.general import get_current_user, current_milli_time
from fastapi.requests import Request
from app.service.parser_service.parser_service import CodeParserService
from app.service.queue_service.queue_service import QueueService
from app.constants.constants import default_queue
from app.core.setup_sql import get_db
from app.repository.repository_repo.repository_repo import RepositoryRepo
from sqlalchemy.exc import IntegrityError

router = APIRouter()
repository_service = RepositoryService()
auth_service = AuthService()
code_parser_service = CodeParserService()
queue_service = QueueService()
odin_queue = queue_service.get_queue(default_queue)


@router.post("/process", dependencies=[Depends(AuthMiddleware.check_auth)])
async def process(request: Request, repository_request: RepositoryProcessRequest, db=Depends(get_db)):
    try:
        url = repository_request.url
        user_id = get_current_user(request)
        repository_base = {
            'url': url,
            'status': 'QUEUED',
            'user_id': user_id,
        }
        repository_repo = RepositoryRepo()
        created_repo_entity = repository_repo.create_repository(repository_base)
        queue_service.send_message(odin_queue, json.dumps(created_repo_entity.to_json()))
        return JSONResponse(
            content={
                'status': "SUCCESS",
                'data': {
                    'identifier': created_repo_entity.id
                },
                'message': "Use the identifier to check the status of result"
            },
            status_code=200
        )
    except IntegrityError as e:
        return JSONResponse(
            content={
                'status': 'ERROR',
                'message': e.orig.args[1]
            },
            status_code=409
        )
    except Exception as e:
        return JSONResponse(
            content={
                'status': 'ERROR',
                'message': str(e)
            },
            status_code=400
        )


@router.get("/get_status", dependencies=[Depends(AuthMiddleware.check_auth)])
async def dumb(request: Request, identifier_id: int, db=Depends(get_db)):
    try:
        repository_repo = RepositoryRepo()
        repository = repository_repo.get_repository_by_id(identifier_id)
        if repository:
            if repository.user_id != get_current_user(request):
                return JSONResponse(
                    content={
                        'status': 'ERROR',
                        'message': 'You are not authorized to view this repository'
                    },
                    status_code=403
                )

            return JSONResponse(
                content={
                    'status': "SUCCESS",
                    'data': repository.to_json()
                },
                status_code=200
            )

        return JSONResponse(
            content={
                'status': 'ERROR',
                'message': 'Repository not found'
            },
            status_code=404
        )
    except Exception as e:
        return JSONResponse(
            content={
                'status': 'ERROR',
                'message': str(e)
            },
            status_code=400
        )
