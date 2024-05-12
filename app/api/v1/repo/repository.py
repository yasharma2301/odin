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
        repository_repo = RepositoryRepo(db)
        created_repo_entity = repository_repo.create_repository(repository_base)
        queue_service.send_message(odin_queue, json.dumps(created_repo_entity.to_json()))
        return JSONResponse(
            content={'status': "SUCCESS", 'identifier': created_repo_entity.id},
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


@router.post("/dumb")
async def dumb(request: Request):
    return repository_service.walk_repository_and_collect_results()
    # return code_parser_service.parse_file()
    # folder_name = f"{get_current_user(request)}-{current_milli_time()}"
    # repository_service.clone_local(url, folder_name)
    # queue_service.send_message(odin_queue, {})
