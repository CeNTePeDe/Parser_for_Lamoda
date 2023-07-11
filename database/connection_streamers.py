import logging
from typing import Optional

from pymongo.collection import Collection

from core.base_class import AbstractDAO
from core.constant_variables import db
from models.streamers_models import StreamerIn, StreamerOut

logger = logging.getLogger(__name__)


class StreamerDAO(AbstractDAO):
    collection: Collection

    def __init__(self):
        self.collection: Collection = db["streamers"]
        super().__init__(self.collection)

    def get_item(self, id: str) -> Optional[StreamerIn]:
        streamer_data = self.collection.find_one({"id": id})
        if streamer_data is None:
            return None
        return StreamerIn(**streamer_data)

    def create_item(self, streamer_data: StreamerIn):
        streamer_dict = streamer_data.dict()
        logger.info("create streamer")
        streamer = self.collection.find_one({"id": streamer_dict["id"]})
        if streamer is None:
            new_streamer = self.collection.insert_one(streamer_dict)
            logger.info(f"new_streamer {new_streamer}")
            return new_streamer

        updated_streamer = self.update_item(streamer_dict["id"], streamer_data)
        logger.info(f"updated streamer {updated_streamer}")
        return updated_streamer

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
        if streamer_update.modified_count == 0:
            return None
        return streamer_update.modified_count

    def delete_item(self, id: str) -> int:
        deleted_product = self.collection.delete_one({"id": id})
        return deleted_product.deleted_count
