from pydantic import BaseModel


class UserBase(BaseModel):
    user_name: str
    uuid: str
    full_name: str
