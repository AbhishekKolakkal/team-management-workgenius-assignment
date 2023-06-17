from pydantic import BaseModel

class TeamSchema(BaseModel):
    name: str
    description: str
    user_id: int


class UserSchema(BaseModel):
    name: str
