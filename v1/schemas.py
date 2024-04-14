from pydantic import BaseModel


class User(BaseModel):
    username: str | None = None


class NewShort(BaseModel):
    url: str
    code: str | None = None


class EditShort(BaseModel):
    url: str
