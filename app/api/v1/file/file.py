from fastapi import APIRouter, Depends
from app.repository.file_repo.file_repo import FileRepo
from fastapi.responses import JSONResponse
from app.repository.repository_repo.repository_repo import RepositoryRepo
from sqlalchemy.exc import IntegrityError
from app.service.queue_service.queue_service import QueueService
from app.constants.constants import default_queue
import json

router = APIRouter()

queue_service = QueueService()
odin_queue = queue_service.get_queue(default_queue)

router = APIRouter()
file_repo = FileRepo()


@router.post("/test")
def test():
    queue_service.send_message(odin_queue, json.dumps({'hi':1}))

    # file_data = {
    #     'repository_id': 1,
    #     'file_extension': '.py',
    #     'file_name': 'my_file',
    #     'parent_folder_path': '/root',
    #     'status': 'COMPLETED',
    #     'error': None,
    #     'metadata': [
    #         {
    #             'function_name': 'my_function',
    #             'function_code': 'def my_function(): pass',
    #             'function_type': 'fun',
    #             'class_name': 'MyClass',
    #         }
    #     ]
    # }
    # file_repo.create_files([file_data])
    return JSONResponse(
        content={},
        status_code=201
    )
