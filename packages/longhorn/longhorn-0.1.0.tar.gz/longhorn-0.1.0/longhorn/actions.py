import logging
from bovine.activitystreams.utils import is_public

from .database import DatabaseContext
from .store import store_comment

logger = logging.getLogger(__name__)


async def handle(client, data, db_url="sqlite://db.sqlite3"):
    """handle to be used together with `mechanical bull
    <https://pypi.org/project/mechanical-bull/>`_

    Usage:

    .. code-block:: toml


        [username.handlers]
        "longhorn.actions" = { db_url = "sqlite:///path/to/your/blog/db.sqlite3" }


    :param db_url:
        specifies the database to be used. Needs to be the
        one longhorn is configured to."""
    if "type" not in data:
        return

    if data["type"] not in ["Create", "Update", "Delete"]:
        return

    if not is_public(data):
        return

    async with DatabaseContext(db_url):
        if "object" in data:
            data = data["object"]

        logger.info(data)
        if isinstance(data, dict):
            await store_comment(data)
