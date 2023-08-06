import asyncio
import logging
from argparse import ArgumentParser
from bovine import BovineClient

from .config import create_actor, bovine_client_config, get_configuration_variable
from .database import DatabaseContext
from .store import create_post, store_base

from .format.formatter import Formatter
from .format.article import formatter_and_actor_to_create


async def post_article(filename):
    async with DatabaseContext():
        config = await bovine_client_config()
        host = await get_configuration_variable("host")
        host = f"https://{host}/"

        async with BovineClient(config) as actor:
            with open(filename, "r") as fp:
                formatter = Formatter(fp.read(), host)
            await formatter.handle_quotes(actor)

            create = formatter_and_actor_to_create(formatter, actor, host)

            response = await actor.send_to_outbox(create)
            activity = await actor.proxy_element(response.headers["location"])
            obj = activity.get("object")

            for notification in formatter.notifications:
                print(notification)
                await actor.send_to_outbox(
                    actor.activity_factory.create(notification).build()
                )

            db_actor = await create_actor(actor)
            await create_post(
                db_actor,
                formatter,
                obj.get("id"),
            )
            await store_base(obj)


def build_parser():
    parser = ArgumentParser("Posts the content of a markdown file to your blog")
    parser.add_argument("file", help="File to post")
    return parser


def main():
    logging.basicConfig(level=logging.INFO)

    args = build_parser().parse_args()

    asyncio.run(post_article(args.file))


if __name__ == "__main__":
    main()
