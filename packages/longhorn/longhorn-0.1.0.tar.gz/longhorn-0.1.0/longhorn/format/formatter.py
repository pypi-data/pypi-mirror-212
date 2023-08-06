from bs4 import BeautifulSoup
from markdown import Markdown
import re
from datetime import date
from urllib.parse import urljoin


from .mastodon_quoter import MastodonQuoter


class Formatter:
    quote_regexp = re.compile(r"{{(.*?)}}")

    def __init__(self, source, host):
        md_smart = Markdown(
            output_format="html5",
            extensions=["fenced_code", "codehilite", "toc", "smarty"],
        )
        base_md = Markdown(output_format="html5")

        self.source = source
        self.host = host
        self.content_base = base_md.convert(source)
        self.content = md_smart.convert(source)

        self.soup = BeautifulSoup(self.content_base, "html.parser")
        self.tag = []
        self.notifications = []

    def get_title(self):
        return self.soup.find("h1").text

    def get_summary(self):
        return self.soup.find("p").text

    def create_article_object(self, object_factory):
        return object_factory.article(
            content=self.content_base,
            source={
                "content": self.source,
                "mediaType": "text/markdown",
            },
            summary=self.get_summary(),
            name=self.get_title(),
            tag=self.tag,
        )

    async def handle_quotes(self, client):
        quotes = list(set(self.quote_regexp.findall(self.content)))

        for quote in quotes:
            quoter = MastodonQuoter(client, quote)
            self.notifications.append(await quoter.notification(self.url))
            object_link = quoter.object_link()
            self.tag.append(object_link)

            self.content_base = self.content_base.replace(
                "{{" + quote + "}}", object_link["name"], 1
            )
            self.content = self.content.replace(
                "{{" + quote + "}}",
                f"""<div class="oembed">{quoter.oembed_html}</div>""",
                1,
            )

    @property
    def url(self):
        today = date.today().isoformat()
        title = self.get_title().replace(" ", "_")
        title = "".join(x for x in title if x.isalnum() or x == "_")
        path = f"{today}/{title}"
        return urljoin(self.host, path)
