from pydantic import BaseModel


class MetaFile(BaseModel):
    name: str
    data: bytes
    type: str
