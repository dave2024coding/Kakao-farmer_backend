from tortoise.models import Model
from tortoise import fields

class Lecture(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    user = fields.ForeignKeyField("models.User", related_name="lectures")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "lectures"

