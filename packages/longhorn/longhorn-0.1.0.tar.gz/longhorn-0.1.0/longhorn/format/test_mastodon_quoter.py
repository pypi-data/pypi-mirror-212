from unittest.mock import AsyncMock
import pytest

from bovine import BovineClient
from bovine.activitystreams import ObjectFactory

from longhorn.config import (
    bovine_client_config,
)
from longhorn.database import DatabaseContext


from .mastodon_quoter import MastodonQuoter


def test_determine_oembed_url():
    remote_id = "https://mastodon/@actor/1101"
    client = AsyncMock(BovineClient)

    quoter = MastodonQuoter(client, remote_id)

    assert (
        quoter.determine_oembed_url()
        == "https://mastodon/api/oembed?url=https://mastodon/@actor/1101"
    )


async def test_collection_informaiton_mocks():
    remote_id = "https://mastodon/@actor/1101"
    client = AsyncMock(BovineClient)

    quoter = MastodonQuoter(client, remote_id)

    client.proxy_element.side_effect = [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "attributedTo": "https://mastodon/users/actor",
            "cc": "https://mastodon/users/actor/followers",
            "content": "<p>test</p>",
            "id": "https://mastodon/users/actor/statuses/1101",
            "published": "2023-04-07T11:16:24Z",
            "to": "as:Public",
            "type": "Note",
            "url": "https://mastodon/@actor/1101",
        },
        {"id": "https://mastodon/users/actor", "preferredUsername": "alice"},
    ]

    client.client = AsyncMock()
    client.client.get.return_value.json.return_value = {
        "html": '<iframe src="https://mastodon/@actor/1101"></iframe><script src="https://mastodon/embed.js" async="async"></script>',  # noqa F501
    }
    client.information = {"id": "https://local/bob"}
    client.object_factory = ObjectFactory(client=client)

    await quoter.collect_information()

    assert quoter.author == "https://mastodon/users/actor"

    mention = await quoter.mention()
    assert mention == {
        "@context": "https://www.w3.org/ns/activitystreams",
        "type": "Mention",
        "href": "https://mastodon/users/actor",
        "name": "alice@mastodon",
    }

    notification = await quoter.notification("post_url")

    assert notification["type"] == "Event"
    assert notification["to"] == ["https://mastodon/users/actor"]

    object_link = quoter.object_link()

    assert object_link["type"] == "Link"
    assert object_link["href"] == "https://mastodon/users/actor/statuses/1101"


@pytest.mark.skip("network")
async def test_mastodon_quoter():
    remote_id = "https://mas.to/@themilkman/110157246268248470"
    async with DatabaseContext():
        config = await bovine_client_config()
        async with BovineClient(config) as client:
            quoter = MastodonQuoter(client, remote_id)

            await quoter.collect_information()

            assert quoter.oembed_html.startswith(
                '<iframe src="https://mas.to/@themilkman/110157246268248470/embed'
            )
            assert quoter.oembed_html.endswith(
                '<script src="https://mas.to/embed.js" async="async"></script>'
            )

            assert quoter.author == "https://mas.to/users/themilkman"
