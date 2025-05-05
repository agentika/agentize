from pydantic import BaseModel


class UserProfileContext(BaseModel):
    lang: str
    length: int
