from abc import ABC, abstractmethod


class AbstractTraficMonitoring(ABC):

    @abstractmethod
    def get_logs(self):
        return NotImplementedError

    @abstractmethod
    def write_logs(self, logs):
        return NotImplementedError

    @abstractmethod
    def parce_package(self, packet):
        return NotImplementedError

    @abstractmethod
    def monitor(self, packet):
        return NotImplementedError

    @abstractmethod
    def run(self):
        return NotImplementedError


