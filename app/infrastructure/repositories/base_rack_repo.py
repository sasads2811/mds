import abc
from uuid import UUID
from app.domain.rack.entity import Rack


class BaseRackRepo(abc.ABC):
    @abc.abstractmethod
    def get_rack_by_id(self, rack_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def get_device_by_id(self, device_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, rack: Rack):
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, rack: Rack):
        raise NotImplementedError

    @abc.abstractmethod
    def get_rack_devices(self, rack_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def create_rack_device(
        self, rack_id: UUID, device_id: UUID, start_unit: int, end_unit: int
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def get_rack_device_by_rack_and_device_id(self, rack_id: UUID, device_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def get_devices_by_ids(self, device_ids: list):
        raise NotImplementedError

    @abc.abstractmethod
    def get_racks_by_ids(self, rack_ids: list):
        raise NotImplementedError
