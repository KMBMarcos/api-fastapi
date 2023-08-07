from pydantic import BaseModel
from typing import Optional

# Entidad user
class User(BaseModel):
    id: Optional[str]
    username: str
    email: str