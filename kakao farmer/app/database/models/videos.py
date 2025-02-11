from tortoise.models import Model
from tortoise import fields

class Video(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    url = fields.CharField(max_length=500)
    user = fields.ForeignKeyField("models.User", related_name="videos")
    created_at = fields.DatetimeField(auto_now_add=True)
