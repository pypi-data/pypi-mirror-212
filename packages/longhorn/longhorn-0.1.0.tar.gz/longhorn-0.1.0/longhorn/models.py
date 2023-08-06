from tortoise import fields
from tortoise.models import Model


class Actor(Model):
    id = fields.IntField(pk=True)

    actor_id = fields.CharField(max_length=255, unique=True)
    fediverse_handle = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)


class Post(Model):
    id = fields.IntField(pk=True)
    author = fields.ForeignKeyField("models.Actor")

    date = fields.CharField(max_length=255)
    title_part = fields.CharField(max_length=255)

    object_id = fields.CharField(max_length=255, default="missing")

    title = fields.CharField(max_length=255)
    summary = fields.TextField()
    content = fields.TextField()

    created = fields.DatetimeField(auto_now_add=True)
    updated = fields.DatetimeField(auto_now=True)


class Comment(Model):
    id = fields.IntField(pk=True)
    object_id = fields.CharField(max_length=255, unique=True)
    in_reply_to = fields.CharField(max_length=255, null=True)
    content = fields.JSONField()


class ConfigurationVariable(Model):
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=255, unique=True)
    value = fields.CharField(max_length=255)
