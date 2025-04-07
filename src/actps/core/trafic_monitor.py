from abc import ABC, abstractmethod


class AbstractTraficMonitoring(ABC):

    @abstractmethod
    def get_logs(self):
        raise NotImplementedError

    @abstractmethod
    def write_logs(self, logs):
        raise NotImplementedError

    @abstractmethod
    def parce_package(self, packet):
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
    def ipv6_parce(self, packet):
        raise NotImplementedError

    @abstractmethod
    def arp_parce(self, packet):
        raise NotImplementedError

    @abstractmethod
    def http_parse(self, packet):
        raise NotImplementedError

    @abstractmethod
    def dns_parse(self, packet):
        raise NotImplementedError
