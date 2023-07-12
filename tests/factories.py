import random

import factory
from faker import Faker

from models.streamers_models import StreamerIn

faker = Faker()


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
    started_at = ""
    language = None
    thumbnail_url = factory.Faker("url")
    tag_ids = []
    tags = []
    is_mature = random.choice([True, False])
