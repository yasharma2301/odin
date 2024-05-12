from fastapi import APIRouter, Depends
from app.repository.file_repo.file_repo import FileRepo
from fastapi.responses import JSONResponse

router = APIRouter()
file_repo = FileRepo()


@router.post("/test")
def test():
    file_data = {
        'repository_id': 1,
        'file_extension': '.py',
        'file_name': 'my_file',
        'parent_folder_path': '/root',
        'status': 'COMPLETED',
        'error': None,
        'metadata': [
            {
                'function_name': 'my_function',
                'function_code': 'def my_function(): pass',
                'function_type': 'fun',
                'class_name': 'MyClass',
            }
        ]
    }
    file_repo.create_files([file_data])
    return JSONResponse(
        content={},
        status_code=201
    )
