from unittest.mock import AsyncMock
import pytest

from .actions import handle
from .models import Comment
from .store import store_base
from .test_store import store  # noqa F811


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"type": "Like", "object": "test"},
        {"type": "Create"},
        {"type": "Create", "to": "someone"},
        {"type": "Create", "to": "as:Public"},
        {"type": "Create", "to": "as:Public", "object": "Test"},
        {
            "type": "Create",
            "to": "as:Public",
            "object": {"type": "Note", "content": "Test"},
        },
    ],
)
async def test_handle_event_nothing_happens(store, data):  # noqa F401
    await handle(AsyncMock(), data, db_url=store)

    assert await Comment.filter().count() == 0


async def test_handle_event_something_happens(store):  # noqa F401
    base = {"id": "base_id"}
    await store_base(base)

    data = {
        "type": "Create",
        "to": "as:Public",
        "object": {"type": "Note", "id": "comment_id", "inReplyTo": "base_id"},
    }

    await handle(AsyncMock(), data, db_url=store)

    assert await Comment.filter().count() == 2
