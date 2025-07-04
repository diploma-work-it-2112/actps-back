from abc import ABC, abstractmethod


class AbstractTraficMonitoring(ABC):

    @abstractmethod
    def get_logs(self):
        raise NotImplementedError

    @abstractmethod
    def write_logs(self, logs):
        raise NotImplementedError

    @abstractmethod
    def monitor(self, packet):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError


class AbstractTraficParser(ABC):

    @abstractmethod
    def parce(self, packet):
        raise NotImplementedError 

    @abstractmethod
    def ether_parse(self, packet):
        raise NotImplementedError

    @abstractmethod
    def ip_parse(self, packet):
        raise NotImplementedError

    @abstractmethod
    def tcp_parse(self, packet):
        raise NotImplementedError

    @abstractmethod
    def udp_parse(self, packet):
        raise NotImplementedError

    @abstractmethod
    def icmp_parse(self, packet):
        raise NotImplementedError

    @abstractmethod
    def ipv6_parse(self, packet):
        raise NotImplementedError

    @abstractmethod
    def arp_parse(self, packet):
        raise NotImplementedError

    @abstractmethod
    def http_parse(self, packet):
        raise NotImplementedError

    @abstractmethod
    def dns_parse(self, packet):
        raise NotImplementedError


class AbstractTraficStorageManager(ABC):
    @abstractmethod
    def write(self, logs):
        pass

    @abstractmethod
    def ndjson_write(self, logs):
        pass

    @abstractmethod
    def ndjson_read(self, year: int, month: int, day: int, start_hour:int, end_hour: int, depth: int):
        pass
