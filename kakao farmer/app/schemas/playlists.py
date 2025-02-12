from pydantic import BaseModel, HttpUrl
from datetime import datetime


class PlaylistCreate(BaseModel):
    title: str
    description: str
    video_ids: list[int]
    url_thumb: HttpUrl
    

# class FormationResponse(BaseModel):
#     id: int
#     title: str
#     description: str
#     video_ids: list[int]
#     created_at: datetime
#     updated_at: datetime
#     user_id: int

#     class Config:
#         from_attributes = True


from tortoise.contrib.pydantic import pydantic_model_creator
from app.database.models import Playlist

PlaylistResponse = pydantic_model_creator(Playlist, name="PlaylistResponse")