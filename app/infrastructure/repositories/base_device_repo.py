import abc
from uuid import UUID
from app.domain.device.entity import Device


class BaseDeviceRepository(abc.ABC):
    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_device_by_id(self, device_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, device: Device):
        raise NotImplementedError

    @abc.abstractmethod
    def save(self, device: Device):
        raise NotImplementedError
