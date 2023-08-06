import logging

from quart import Quart
from tortoise.contrib.quart import register_tortoise

from longhorn.blueprint import blueprint
from longhorn.config import TORTOISE_ORM, configure_app

logging.basicConfig(level=logging.INFO)


app = Quart(__name__)
app.register_blueprint(blueprint)


@app.before_first_request
async def startup():
    await configure_app(app)


register_tortoise(
    app,
    db_url=TORTOISE_ORM["connections"]["default"],
    modules={"models": TORTOISE_ORM["apps"]["models"]["models"]},
    generate_schemas=False,
)


def main():
    app.run()


if __name__ == "__main__":
    main()
