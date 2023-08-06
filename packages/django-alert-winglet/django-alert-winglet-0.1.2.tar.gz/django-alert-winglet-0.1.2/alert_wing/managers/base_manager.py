from abc import ABC, abstractmethod


class BaseManager(ABC):
    @abstractmethod
    def format_exception(self) -> tuple[str, str]:
        raise NotImplementedError

    @abstractmethod
    def set_data_for_delivery(self):
        ...
