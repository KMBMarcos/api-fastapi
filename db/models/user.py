from pydantic import BaseModel

# Entidad user
class User(BaseModel):
    id: str | None
    username : str
    email :str