from tortoise.models import Model
from tortoise import fields

class Playlist(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    url_thumb = fields.CharField(max_length=500)
    prix = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    video_count = fields.IntField(default=0)
    user = fields.ForeignKeyField("models.User", related_name="playlists")
    videos = fields.ManyToManyField("models.Video", related_name="playlists")

    class Meta:
        table = "playlists"

