import random

import factory
from faker import Faker

from models.product_models import CategoryModel, ProductModel
from models.streamers_models import StreamerIn

faker = Faker()


class CategoryFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = CategoryModel

    category = "test_category"


class ProductFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = ProductModel

    name_product = factory.Sequence(lambda n: f"product_{n}")
    picture_link = factory.Faker("url")
    price = str(random.uniform(50.0, 500.0))
    product_detail_link = factory.Faker("url")
    characteristic = {}
    description = factory.Sequence(lambda n: f"description_{n}")
    category = factory.SubFactory(CategoryFactory)
    product_id = factory.Sequence(lambda n: f"id_{n}")


class StreamerInFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = StreamerIn

    id = factory.Sequence(lambda n: f"id_{n}")
    user_id = factory.Sequence(lambda n: f"user_id_{n}")
    user_login = factory.Sequence(lambda n: f"user_login_{n}")
    user_name = factory.Sequence(lambda n: f"user_name_{n}")
    game_id = factory.Sequence(lambda n: f"game_id_{n}")
    game_name = factory.Sequence(lambda n: f"name_game_{n}")
    type = "live"
    title = factory.Sequence(lambda n: f"title_{n}")
    viewer_count = random.randint(0, 1000)
    started_at = "2023-07-14T09:56:25Z"
    language = None
    thumbnail_url = factory.Faker("url")
    tag_ids = []
    tags = ["str", "str"]
    is_mature = False
