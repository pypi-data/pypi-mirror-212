import pytest

from bovine import BovineClient

from longhorn.config import (
    bovine_client_config,
)
from longhorn.database import DatabaseContext

from .formatter import Formatter


raw = (
    """#  Title

This is the introduction

## More content

"""
    + "abcdef " * 100
)


def test_formatter():
    formatter = Formatter(raw, "http://localhost")

    assert formatter.get_title() == "Title"
    assert formatter.get_summary() == "This is the introduction"


raw_with_oembed = """# Oembed

Isn't this great?

## The iframe

<iframe
    src="https://mas.to/@helgek/110037996902548557/embed"
    class="mastodon-embed"
    style="max-width: 100%; border: 0"
    width="600"
    allowfullscreen="allowfullscreen"
></iframe>
<script src="https://mas.to/embed.js" async="async"></script>

huh?"""


async def test_format_with_iframe():
    formatter = Formatter(raw_with_oembed, "http://localhost")

    assert formatter.get_title() == "Oembed"
    assert formatter.get_summary() == "Isn't this great?"

    assert "</iframe>" in formatter.content
    assert "</script>" in formatter.content


raw_with_quote = """# Quote

Isn't this great?

## The quote

{{https://mas.to/@themilkman/110157246268248470}}

huh?"""


@pytest.mark.skip("network")
async def test_format_with_quote():
    async with DatabaseContext():
        config = await bovine_client_config()
        async with BovineClient(config) as client:
            formatter = Formatter(raw_with_quote, "http://localhost")

            await formatter.handle_quotes(client)

            assert formatter.get_title() == "Quote"
            assert formatter.get_summary() == "Isn't this great?"

            assert (
                "RE: https://mas.to/@themilkman/110157246268248470"
                in formatter.content_base
            )
            assert "</iframe>" in formatter.content
            assert "</script>" in formatter.content


def test_formatter_url():
    formatter = Formatter(
        """# this is atitle

text""",
        "https://mymath.rocks",
    )
    url = formatter.url
    assert url.startswith("https://mymath.rocks/")
    assert url.endswith("/this_is_atitle")

    formatter = Formatter(
        """# a1#ftnb/;'[dA ]x

text""",
        "https://mymath.rocks",
    )
    url = formatter.url
    assert url.startswith("https://mymath.rocks/")
    assert url.endswith("/a1ftnbdA_x")
