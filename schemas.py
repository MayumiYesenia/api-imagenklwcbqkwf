from pydantic import BaseModel
class Image(BaseModel):
    name: str
    description: str
    url :str
