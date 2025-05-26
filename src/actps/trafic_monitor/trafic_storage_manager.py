from abc import abstractmethod
import json 
import datetime
import os

from src.actps.core.cache_service import AbstractCacheService
from src.actps.core.trafic_monitor import AbstractTraficStorageManager


class TraficStorageManager(AbstractTraficStorageManager):

    def __init__(self, file_path: str):
        self._file_path = file_path
        self.log_to_write = {}


    def universal_default(self, o):
        if isinstance(o, bytes):
            try:
                return o.decode('utf-8')
            except UnicodeDecodeError:
                return o.hex()
        return str(o)

    def write(self, logs, hour, minute, cache_service: AbstractCacheService):
        today = datetime.date.today()
        month = today.month  
        day = today.day     
        year = today.year
        self.log_to_write = {}

        self.protocol_count(logs)
        self.ip_count(logs)
        self.mac_count(logs)

        self.ndjson_write(
            log=self.log_to_write,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
        )


    def ndjson_write(self, log, year: int, month: int, day: int, hour: int, minute: int):
        path_to_dir = str(year)+"_"+str(month)+"_"+str(day)

        if not os.path.exists(path_to_dir):
            os.makedirs(path_to_dir) 
        
        if minute <= 30:
            path_file = f"{hour}_30.ndjson" 
        else:
            path_file = f"{hour}_60.ndjson"
        with open(self._file_path+path_to_dir+path_file, "a", encoding="utf-8") as f:
            for log in logs:
                data = json.dumps(log, default=self.universal_default, ensure_ascii=False)
                f.write(data+"\n")


    def ndjson_read(self, year: int, month: int, day: int, start_hour: int, end_hour: int, depth: int):
        path_to_file = str(year)+"_"+str(month)+"_"+str(day)+"_packet_logs.ndjson"
        path = self._file_path + path_to_file 

# Если ни start_hour, ни depth не заданы, выбрасываем ошибку
        if start_hour is None and depth is None:
            raise ValueError("incorrect initial data")

        # Вычисляем временные границы (если заданы)
        if start_hour is not None:
            lower_bound = datetime.datetime(year, month, day, start_hour, 0, 0).timestamp()
        if end_hour is not None:
            upper_bound = datetime.datetime(year, month, day, end_hour, 0, 0).timestamp()

        logs = []
        count_log = 0

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    log = json.loads(line)
                except Exception:
                    continue

                if "time" not in log:
                    continue

                t = float(log["time"])

                if start_hour is not None and end_hour is not None:
                    if lower_bound <= t <= upper_bound:
                        logs.append(log)
                    elif t > upper_bound:
                        break
                else:
                    logs.append(log)

                count_log += 1
                if depth is not None and count_log >= depth:
                    break

        return logs


    def protocol_count(self, logs):
        num_protocols = {
            "Ether": 0,
            "IPv4": 0,
            "TCP": 0,
            "UDP": 0,
            "ICMP": 0,
            "IPv6": 0,
            "ARP": 0,
            "DNS": 0,
            "HTTP": 0,
            "HTTPS": 0,
            "Unknown": 0
        }

        for pkt in logs:
            proto = 'Unknown'

            if not isinstance(pkt, dict):
                print(None)
                continue

            if any(k.startswith('dns_') for k in pkt):
                proto = 'DNS'
            elif 'http_payload' in pkt or 'http_headers' in pkt:
                proto = 'HTTP'
            elif 'https_payload_hex' in pkt:
                proto = 'HTTPS'
            elif any(k.startswith('icmp_') for k in pkt):
                proto = 'ICMP'
            elif any(k.startswith('tcp_') for k in pkt):
                proto = 'TCP'
            elif any(k.startswith('udp_') for k in pkt):
                proto = 'UDP'
            elif any(k.startswith('ipv6_') for k in pkt):
                proto = 'IPv6'
            elif any(k.startswith('ip_') for k in pkt):
                proto = 'IPv4'
            elif any(k.startswith('arp_') for k in pkt):
                proto = 'ARP'
            elif any(k.startswith('mac_') for k in pkt):
                proto = 'Ether'

            num_protocols[proto] += 1

        data_to_save = {
            "num_proto": num_protocols
        }

        self.log_to_write.update(data_to_save)


    def ip_count(self, logs):
        ips_src = {}
        ips_dst = {}

        for pkt in logs:
            
            if not instance(pkt, dict):
                continue 

            if "ip_src" in pkt:
                if pkt["ip_src"] not in ips_src:
                    ips_src[pkt["ip_src"]] = 1
                else:
                    ips_src[pkt["ip_src"]] += 1
            elif "ipv6_src" in pkt:
                if pkt["ipv6_src"] not in ips_src:
                    ips_src[pkt["ipv6_src"]] = 1
                else:
                    ips_src[pkt["ipv6_src"]] += 1 
            
            if "ip_dst" in pkt:
                if pkt["ip_dst"] not in ips_dst:
                    ips_dst[pkt["ip_dst"]] = 1 
                else:
                    ips_dst[pkt["ip_dst"]] += 1
            elif "ipv6_dst" in pkt:
                if pkt["ipv6_dst"] not in ips_dst:
                    ips_dst[pkt["ipv6_dst"]] = 1
                else:
                    ips_dst[pkt["ipv6_dst"]] += 1
        
        data_to_save = {
            "ips_src": ips_src,
            "ips_dst": ips_dst
        }

        self.log_to_write.update(data_to_save)


    def mac_count(self, logs):
        macs_src = {}
        macs_dst = {}

        for pkt in logs:
            if not isinstance(pkt, dict):
                continue

            if "mac_src" in pkt:
                if pkt["mac_src"] not in macs_src:
                    macs_src[pkt["mac_src"]] = 1
                else:
                    macs_src[pkt["mac_src"]] += 1

            if "mac_dst" in pkt:
                if pkt["mac_dst"] not in macs_dst:
                    macs_dst[pkt["mac_dst"]] = 1
                else:
                    macs_dst[pkt["mac_dst"]] += 1

        data_to_save = {
            "macs_src": macs_src,
            "macs_dst": macs_dst
        }

        self.log_to_write.update(data_to_save)

    def process_name_by_port_count(self, logs, cache_service: AbstractCacheService):

        process_names = {}

        for pkt in logs:
            if "tcp_sport" in pkt or "udp_sport" in pkt:
                sport = pkt.get("tcp_sport") or pkt.get("udp_sport")
                ip_src = pkt.get("ip_src")
                if ip_src:
                    port_processes = cache_service.hgetall(ip_src)
                    process_name = port_processes.get(str(sport))
                    if process_name:
                        process_names[process_name] = process_names.get(process_name, 0) + 1

            if "tcp_dport" in pkt or "udp_dport" in pkt:
                dport = pkt.get("tcp_dport") or pkt.get("udp_dport")
                ip_dst = pkt.get("ip_dst")
                if ip_dst:
                    port_processes = cache_service.hgetall(ip_dst)
                    process_name = port_processes.get(str(dport))
                    if process_name:
                        process_names[process_name] = process_names.get(process_name, 0) + 1

        return process_names




