from pydantic import BaseModel
from datetime import datetime


class FormationCreate(BaseModel):
    title: str
    description: str

class FormationResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True