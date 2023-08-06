import logging
from urllib.parse import urljoin

from quart import Blueprint, current_app, render_template, request, send_from_directory
from feedwerk.atom import AtomFeed

from .format.for_web import sanitize
from .models import Post
from .store import retrieve_thread, formatted_posts

blueprint = Blueprint("bovine_blog_blueprint", __name__)

logger = logging.getLogger(__name__)


@blueprint.get("/")
async def main():
    formatted, posts = await formatted_posts()
    if len(posts) > 0:
        fediverse_handle = posts[0].author.fediverse_handle
    else:
        fediverse_handle = "please post"

    blog_title = current_app.config["blog_title"]

    return await render_template(
        "index.html",
        posts=formatted,
        blog_title=blog_title,
        fediverse_handle=fediverse_handle,
        posts_side=formatted[:10],
    )


@blueprint.get("/atom.xml")
async def atom_feed():
    _, posts = await formatted_posts()

    feed = AtomFeed(current_app.config["blog_title"], feed_url=request.url)

    for x in posts:
        feed.add(
            x.title,
            x.summary,
            url=urljoin(request.url, f"/{x.date}/{x.title_part}"),
            updated=x.updated,
        )

    return feed.get_response()


@blueprint.get("/static/<filename>")
async def static_resource(filename):
    if filename not in ["home.css", "styles.css", "background.jpg"]:
        return "", 404
    return await send_from_directory("static", filename)


async def is_activity_request():
    accept_header = request.headers.get("Accept")
    if not accept_header:
        return False

    return "json" in accept_header


@blueprint.get("/<date>/<title>")
async def display_post(date, title):
    formatted, _ = await formatted_posts()
    post = await Post.get_or_none(date=date, title_part=title).prefetch_related(
        "author"
    )
    if post is None:
        return "not found", 404

    fediverse_handle = post.author.fediverse_handle

    blog_title = current_app.config["blog_title"]
    page_title = f"{blog_title}: {post.title}"

    thread = await retrieve_thread(post.object_id)

    thread = await sanitize(thread)

    return await render_template(
        "page.html",
        content=post.content,
        page_title=page_title,
        entry=thread,
        object_id=post.object_id,
        blog_title=blog_title,
        fediverse_handle=fediverse_handle,
        posts_side=formatted[:10],
    )
