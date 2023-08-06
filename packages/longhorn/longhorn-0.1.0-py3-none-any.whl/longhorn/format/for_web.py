from datetime import datetime
from urllib.parse import urlparse
import bleach

from longhorn.models import Actor


def clean_content(content):
    if content is None:
        return ""
    content = bleach.clean(content, tags=[], strip=True)
    content = content.replace("\n\n", "\n")
    return content.replace("\n", "<br/><br/>")


def format_published(published):
    try:
        return datetime.fromisoformat(published[:-1]).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return ""


async def format_actor(actor):
    db_actor = await Actor.get_or_none(actor_id=actor)

    if db_actor:
        return db_actor.fediverse_handle

    return "@" + actor.split("/")[-1] + "@" + urlparse(actor).netloc


async def sanitize(thread):
    if thread is None:
        return {"content": {}, "replies": []}
    content = thread["content"]
    actor = content.get("attributedTo")

    if actor:
        username = await format_actor(actor)
    else:
        username = None

    return {
        "content": {
            **content,
            "published": format_published(content.get("published")),
            "username": username,
            "content": clean_content(content.get("content")),
        },
        "replies": [await sanitize(x) for x in thread["replies"]],
    }
