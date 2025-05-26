from scapy.all import sniff, Ether, IP, TCP, UDP, ICMP, Raw, ARP, IPv6, DNS, DNSQR
from datetime import datetime
import time
import json
import requests

from src.actps.core.cache_service import AbstractCacheService
from src.actps.core.trafic_monitor import AbstractTraficMonitoring, AbstractTraficParser, AbstractTraficStorageManager
from src.actps.config import IP_BLOCK_LIST_FILE_PATH


class TraficMonitor(AbstractTraficMonitoring):

    def __init__(self, log_writer: AbstractTraficStorageManager, log_parser: AbstractTraficParser, cache_service: AbstractCacheService, stream_key, stream_key_stat):
        self.logs = []
        self.log_writer = log_writer
        self.log_parser = log_parser
        self.cache_service = cache_service
        self.stream_key = stream_key
        self.stream_key_stat = stream_key_stat

        self.tcp_count = 0
        self.arp_count = 0
        self._time = time.time()
        self._log_time_s = 0


    def block_address(self, addr):
        requests.get("http://"+addr+":8080/close-connection") 

    def monitor_freq(self, packet_json):
        if packet_json is None:
            return 
        if any(k.startswith('tcp_') for k in packet_json):
            self.tcp_count += 1 
        elif any(k.startswith('arp_') for k in packet_json):
            self.arp_count += 1


        if int(time.time()) - int(self._time) >= 1:
            print("if")
            if self.tcp_count >= 200:
                print("DDOS")
                print(packet_json)
                print(packet_json["ip_src"])
                self.block_address(packet_json["ip_src"])
                time.sleep(20)
            if self.arp_count >= 200:
                print("namp")
                print(packet_json["arp_psrc"])
                self.block_address(packet_json["arp_psrc"])
            self._time = time.time()
            self.tcp_count = 0
            self.arp_count = 0

    def monitor(self, packet):

        if packet is None:
            print("None")
            return
        log = self.log_parser.parce(packet)
        self.logs.append(log)
        log_time = log["time"]
        log_time_dt = datetime.fromtimestamp(log_time)
        log_sec = log_time_dt.second
        log_hour = log_time_dt.hour
        log_minutes = log_time_dt.minute

        print(log_minutes, log_sec, self._log_time_s)
        
        if log_sec % 5 == 0 and self._log_time_s != log_sec:
            # print(log_minutes, log_sec)
            self.write_logs(log_hour, log_minutes)
            self._log_time_s = log_sec

        
        # self.monitor_freq(log)

        self.cache_service.xadd(self.stream_key, log)
        cache_len = self.cache_service.xlen(self.stream_key)

        if cache_len >= 150:
            self.cache_service.xtrim(self.stream_key, 100)

        # if len(self.logs) == 100:
        #     print("write")
        #     self.write_logs()


    def run(self):
        try:
            sniff(prn=self.monitor, store=False)
        except Exception as e:
            print(1)
            print(e)
            print("Trafic Monitor Process Error")



    def get_logs(self):
        pass

    
    def write_logs(self, hour, minute):
        self.log_writer.write(self.logs, hour, minute, self.cache_service)
        self.logs = []
