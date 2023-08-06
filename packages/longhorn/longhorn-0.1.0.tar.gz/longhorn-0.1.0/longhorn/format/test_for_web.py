from .for_web import format_actor, format_published, sanitize
from longhorn.models import Actor
from longhorn.test_store import store  # noqa F801


def test_format_published():
    formatted = format_published("2023-03-16T07:37:37Z")

    assert formatted == "2023-03-16 07:37"


async def test_format_actor(store):  # noqa F401
    formatted = await format_actor("https://domain/users/name")

    assert formatted == "@name@domain"


async def test_format_actor_in_database(store):  # noqa F401
    await Actor.create(
        actor_id="https://domain/xxxxxxxxx",
        fediverse_handle="@name@domain",
        name="name",
    )

    formatted = await format_actor("https://domain/xxxxxxxxx")

    assert formatted == "@name@domain"


async def test_sanitize(store):  # noqa F401
    thread = {
        "content": {"content": "", "published": "", "username": None},
        "replies": [],
    }

    assert (await sanitize(thread)) == thread
