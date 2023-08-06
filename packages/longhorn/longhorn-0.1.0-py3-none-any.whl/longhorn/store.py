from .models import Comment, Post


async def create_post(actor, formatter, object_id):
    date, title_part = formatter.url.split("/")[-2:]

    await Post.create(
        author=actor,
        content=formatter.content,
        summary=formatter.get_summary(),
        title=formatter.get_title(),
        date=date,
        title_part=title_part,
        object_id=object_id,
    )


async def store_base(obj):
    object_id = obj.get("id")

    if object_id is None:
        return

    return await Comment.create(object_id=object_id, content=obj)


async def store_comment(obj):
    object_id = obj.get("id")
    in_reply_to = obj.get("inReplyTo")

    if in_reply_to is None or object_id is None:
        return

    reply_to = await Comment.get_or_none(object_id=in_reply_to)
    if reply_to is None:
        return

    return await Comment.update_or_create(
        object_id=object_id, defaults={"in_reply_to": in_reply_to, "content": obj}
    )


async def retrieve_thread(object_id):
    base_object = await Comment.get_or_none(object_id=object_id)

    if base_object is None:
        return None

    return await with_replies(base_object)


def format_content(content):
    keys = ["content", "tag", "attributedTo", "url", "published"]
    return {key: content[key] for key in keys if key in content}


async def with_replies(obj):
    object_id = obj.object_id
    replies = await Comment.filter(in_reply_to=object_id).all()

    return {
        "content": format_content(obj.content),
        "replies": [await with_replies(x) for x in replies],
    }


async def formatted_posts():
    posts = await Post.filter().order_by("-created").prefetch_related("author").all()

    formatted = [
        {
            "title": x.title,
            "summary": x.summary,
            "date": x.date,
            "title_part": x.title_part,
        }
        for x in posts
    ]

    return formatted, posts
