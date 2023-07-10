from abc import ABC, abstractmethod

from bson import ObjectId


class AbstractDAO(ABC):
    def __init__(self, collection):
        self.collection = collection

    @abstractmethod
    def get_all_items(self):
        return self.collection.find()

    @abstractmethod
    def get_item(self, _id):
        item_id = ObjectId("_id")
        item = self.collection.find_one({"_id": {"$eq": item_id}})
        return item

    @abstractmethod
    def create_item(self, item):
        raise NotImplementedError("Subclasses must implement create_item method")

    @abstractmethod
    def update_item(self, _id, item):
        raise NotImplementedError("Subclasses must implement update_item method")

    @abstractmethod
    def delete_item(self, _id):
        raise NotImplementedError("Subclasses must implement delete_item method")
