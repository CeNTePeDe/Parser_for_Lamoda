from abc import ABC, abstractmethod


class AbstractDAO(ABC):
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def create(self, item):
        pass

    @abstractmethod
    def update(self, _id, item):
        pass

    @abstractmethod
    def delete(self, _id):
        pass
