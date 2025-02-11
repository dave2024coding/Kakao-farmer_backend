from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class VideoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    url: HttpUrl

class VideoResponse(VideoCreate):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
