def formatter_and_actor_to_create(formatter, actor, host):
    activity_factory, object_factory = actor.factories
    article = formatter_and_activity_factory_to_article(formatter, object_factory, host)
    create = activity_factory.create(article).build()

    return create


def formatter_and_activity_factory_to_article(formatter, object_factory, host):
    article = formatter.create_article_object(object_factory).as_public()
    article.url = formatter.url
    return article.build()
