from tortoise import Tortoise


class DatabaseContext:
    def __init__(self, db_url="sqlite://db.sqlite3"):
        self.db_url = db_url

    async def __aenter__(self):
        await Tortoise.init(db_url=self.db_url, modules={"models": ["longhorn.models"]})

    async def __aexit__(self, *args):
        await Tortoise.close_connections()
