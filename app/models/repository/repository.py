from pydantic import BaseModel


class RepositoryProcessRequest(BaseModel):
    url: str
