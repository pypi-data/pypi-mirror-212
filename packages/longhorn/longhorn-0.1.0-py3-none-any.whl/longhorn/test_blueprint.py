import pytest

from quart import Quart

from .test_store import store  # noqa F401
from .blueprint import blueprint
from .models import Post, Actor


@pytest.fixture
async def test_app(store):  # noqa F801
    app = Quart(__name__)
    app.register_blueprint(blueprint)
    app.config["blog_title"] = "Test blog title"

    yield app


async def test_main(test_app):
    actor = await Actor.create(
        actor_id="https://abel/alice", fediverse_handle="alice@abel", name="Alice"
    )
    await Post.create(
        author=actor,
        date="2023-06-06",
        title_part="Test_post",
        title="Test Post",
        summary="This is a post to test main page is working",
        content="no content",
    )

    async with test_app.test_client() as client:
        response = await client.get("/")

        assert response.status_code == 200
        content = (await response.get_data()).decode("utf-8")

        assert "Test blog title" in content

        assert "Test Post" in content
        assert "This is a post to test main page is working" in content


async def test_atomxml(test_app):
    actor = await Actor.create(
        actor_id="https://abel/alice", fediverse_handle="alice@abel", name="Alice"
    )
    await Post.create(
        author=actor,
        date="2023-06-06",
        title_part="Test_post",
        title="Test Post",
        summary="This is a post to test main page is working",
        content="no content",
    )

    async with test_app.test_client() as client:
        response = await client.get("/atom.xml")

        assert response.status_code == 200
        content = (await response.get_data()).decode("utf-8")

        assert "Test blog title" in content

        assert "Test Post" in content
        assert "This is a post to test main page is working" in content
