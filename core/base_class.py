from abc import ABC, abstractmethod

from bson import ObjectId


class AbstractDAO(ABC):
    def __init__(self, collection):
        self.collection = collection

    @abstractmethod
    def get_all_item(self):
        return self.collection.find()

    @abstractmethod
    def get_item(self, _id):
        item_id = ObjectId("_id")
        item = self.collection.find_one({"_id": {"$eq": item_id}})
        return item

    @abstractmethod
    def create_item(self, item):
        pass

    @abstractmethod
    def update_item(self, _id, item):
        pass

    @abstractmethod
    def delete_item(self, _id):
        pass
