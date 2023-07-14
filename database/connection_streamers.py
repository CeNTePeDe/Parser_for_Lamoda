import logging
from typing import Optional

from pymongo.collection import Collection

from config.settings import db
from core.base_class import AbstractDAO
from models.streamers_models import StreamerIn, StreamerOut

logger = logging.getLogger(__name__)


class StreamerDAO(AbstractDAO):
    collection: Collection

    def __init__(self):
        self.collection: Collection = db["streamers"]
        super().__init__(self.collection)

    def get_item(self, id: str) -> Optional[StreamerIn]:
        streamer_data = self.collection.find_one({"id": id})
        return StreamerIn(**streamer_data) if streamer_data else None

    def create_item(self, streamer_data: StreamerIn) -> StreamerIn:
        streamer_dict = streamer_data.dict()
        logger.info("create streamer")
        streamer = self.collection.find_one({"id": streamer_dict["id"]})
        if streamer is None:
            new_streamer = self.collection.insert_one(streamer_dict)
            logger.info(f"new_streamer {new_streamer}")
            streamer = self.collection.find_one({"_id": new_streamer.inserted_id})
            return StreamerIn(**streamer)

        self.update_item(streamer_dict["id"], streamer_data)
        streamer = self.collection.find_one({"id": streamer_dict["id"]})
        return StreamerIn(**streamer)

    def sort_item(self) -> list[StreamerOut]:
        sort_streamer = self.collection.find().sort("viewer_count", -1)
        return [StreamerOut(**item) for item in sort_streamer]

    def get_all_items(self) -> list[StreamerOut]:
        collection = self.collection.find()
        list_streamers = [StreamerOut(**item) for item in collection]
        return list_streamers

    def update_item(self, id: str, streamer_data: StreamerIn) -> Optional[int]:
        streamer_update = self.collection.update_one(
            {"id": id}, {"$set": streamer_data.dict()}
        )
        return streamer_update.modified_count

    def delete_item(self, id: str) -> int:
        deleted_product = self.collection.delete_one({"id": {"$eq": id}})
        return deleted_product.deleted_count
