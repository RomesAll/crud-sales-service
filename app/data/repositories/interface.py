import uuid
from abc import ABC, abstractmethod
from app.data.models import Base

class Repository(ABC):
    @abstractmethod
    def get_all(self, limit: int = 10, offset: int = 0):
        pass

    @abstractmethod
    def get_by_id(self, id: int | uuid.UUID):
        pass

    @abstractmethod
    def insert(self, orm_object: Base):
        pass

    @abstractmethod
    def update(self, id: int | uuid.UUID, update_data: dict):
        pass

    @abstractmethod
    def delete(self, id: int | uuid.UUID):
        pass