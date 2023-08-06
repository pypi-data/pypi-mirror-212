from urllib.parse import urlparse

import os
import aiohttp
import logging

# from aerich import Command
from bovine import BovineClient
from bovine.crypto import (
    generate_ed25519_private_key,
    private_key_to_did_key,
)
from tortoise import Tortoise

from longhorn.models import Actor, ConfigurationVariable

logger = logging.getLogger(__name__)

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "models": {
            "models": ["longhorn.models"],
            "default_connection": "default",
        },
    },
}


async def configure_app(app):
    session = aiohttp.ClientSession()
    app.config["session"] = session

    app.config["blog_title"] = await get_configuration_variable("blog_title")

    if os.environ.get("NO_EVENT_SOURCE") is None:
        actor = BovineClient(await bovine_client_config())
        await actor.init(session=session)
        app.config["bovine_actor"] = actor


async def create_actor(actor):
    domain = urlparse(actor.information["id"]).netloc
    fediverse_handle = actor.information["preferredUsername"] + "@" + domain

    db_actor, _ = await Actor.get_or_create(
        actor_id=actor.information["id"],
        defaults={
            "fediverse_handle": fediverse_handle,
            "name": actor.information["name"],
        },
    )

    return db_actor


async def get_configuration_variable(key, question=None):
    value = await ConfigurationVariable.get_or_none(key=key)
    if value is None and question:
        value = input(question)
        await ConfigurationVariable.create(key=key, value=value)
    elif value:
        value = value.value

    return value


async def install_or_upgrade():
    # logger.info("Starting Database update or creation")

    # command = Command(tortoise_config=TORTOISE_ORM)
    # await command.init()
    # await command.upgrade()

    # logger.info("Database updated")

    await Tortoise.init(
        db_url="sqlite://db.sqlite3", modules={"models": ["longhorn.models"]}
    )
    await Tortoise.generate_schemas()

    logger.info("Checking Configuration")

    host = await get_configuration_variable(
        "host", "Please enter the hostname your blog will run on: "
    )
    blog_title = await get_configuration_variable(
        "blog_title", "Please enter the title of your blog: "
    )
    activity_pub_host = await get_configuration_variable(
        "activity_pub_host",
        "Please enter the hostname where your ActivityPub Actor is on: ",
    )
    private_key = await get_configuration_variable("private_key")

    if private_key is None:
        private_key = generate_ed25519_private_key()
        did_key = private_key_to_did_key(private_key)
        await ConfigurationVariable.create(key="private_key", value=private_key)
    else:
        did_key = private_key_to_did_key(private_key)

    logger.info("")
    logger.info("--- Current Configuration ---")
    logger.info("Host:        %s", host)
    logger.info("Blog Title:  %s", blog_title)
    logger.info("AP Host:     %s", activity_pub_host)
    logger.info("DID Key:     %s", did_key)

    await Tortoise.close_connections()


async def bovine_client_config():
    activity_pub_host = await get_configuration_variable("activity_pub_host")
    private_key = await get_configuration_variable("private_key")
    return {"host": activity_pub_host, "private_key": private_key}
