from pydantic import BaseModel
from datetime import datetime


class LectureCreate(BaseModel):
    title: str
    description: str
    content: str

class LectureResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    user_id: int

    class Config:
        from_attributes = True


# from tortoise.contrib.pydantic import pydantic_model_creator
# from app.database.models import Formation

# FormationResponse = pydantic_model_creator(Formation, name="FormationResponse")