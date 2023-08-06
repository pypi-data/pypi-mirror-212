from unittest.mock import MagicMock

from bovine.activitystreams.activity_factory import ActivityFactory
from bovine.activitystreams.object_factory import ObjectFactory

from .article import (
    formatter_and_activity_factory_to_article,
    formatter_and_actor_to_create,
)
from .formatter import Formatter


raw = """# Title

This is a summary of something

## Content

This is more content"""


def test_formatter_and_activity_factory_to_article():
    formatter = Formatter(raw, "host")

    object_factory = ObjectFactory({"id": "id", "followers": "followers"})

    article = formatter_and_activity_factory_to_article(
        formatter, object_factory, "host"
    )

    assert "content" in article["content"]
    assert "Title" == article["name"]
    assert "summary" in article["summary"]


def test_formatter_and_actor_to_create():
    info = {"id": "id", "followers": "followers"}
    actor = MagicMock()
    actor.factories = (ActivityFactory(info), ObjectFactory(info))

    formatter = Formatter(raw, "https://host")

    create = formatter_and_actor_to_create(formatter, actor, "https://host")

    assert create["type"] == "Create"
    assert create["actor"] == "id"

    assert create["object"]["name"] == "Title"

    assert create["object"]["url"].startswith("https://host/")
    assert create["object"]["url"].endswith("/Title")
