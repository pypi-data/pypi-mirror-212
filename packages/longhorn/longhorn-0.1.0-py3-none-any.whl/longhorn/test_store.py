import os

import pytest
from tortoise import Tortoise

from .store import retrieve_thread, store_base, store_comment


@pytest.fixture
async def store():
    db_file = "test_db.db"
    db_url = f"sqlite://{db_file}"

    await Tortoise.init(db_url=db_url, modules={"models": ["longhorn.models"]})
    await Tortoise.generate_schemas()

    yield db_url
    await Tortoise.close_connections()
    os.unlink(db_file)


async def test_store_comment_no_base_comment(store):
    obj = {}
    assert await store_comment(obj) is None

    obj = {"id": "id"}
    assert await store_comment(obj) is None

    obj = {"id": "id", "inReplyTo": "unknown"}
    assert await store_comment(obj) is None


async def test_store_comment_base_comment(store):
    base = {"id": "base"}
    await store_base(base)

    obj = {"id": "id", "inReplyTo": "base"}
    assert await store_comment(obj) is not None

    obj = {"id": "id", "inReplyTo": "unknown"}
    assert await store_comment(obj) is None


async def test_store_retrieve_thread(store):
    base = {"id": "base", "content": "XXXX"}
    obj = {"id": "id", "inReplyTo": "base", "content": "YYY"}
    await store_base(base)
    await store_comment(obj)

    result = await retrieve_thread("base")

    assert len(result["replies"]) == 1


async def test_store_retrieve_thread_unknown(store):
    result = await retrieve_thread("unknown")

    assert result is None
