from scapy.all import sniff, Ether, IP, TCP, UDP, ICMP, Raw, ARP, IPv6, DNS, DNSQR
import time

from src.actps.core.trafic_monitor import AbstractTraficMonitoring, AbstractTraficParser


class TraficMonitor(AbstractTraficMonitoring):

    def __init__(self, log_writer, log_parser: AbstractTraficParser):
        self.logs = []
        self.log_writer = log_writer
        self.log_parser = log_parser

    def monitor(self, packet):
        log = self.log_parser.parce(packet)
        self.logs.append(log)

        if len(self.logs) == 100:
            self.write_logs()


    def run(self):
        try:
            sniff(prn=self.monitor, store=False)
        except Exception as e:
            print(1)
            print(e)
            print("Trafic Monitor Process Error")



    def get_logs(self):
        pass

    
    def write_logs(self):
        pass
