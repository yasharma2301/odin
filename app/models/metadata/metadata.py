from pydantic import BaseModel


class Metadata(BaseModel):
    function_type: str
    file_name: str
    file_extension: str
    function_code: str
    function_name: str
    class_name: str
