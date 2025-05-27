from abc import abstractmethod
import json 
import datetime
import os

from src.actps.core.cache_service import AbstractCacheService
from src.actps.core.trafic_monitor import AbstractTraficStorageManager


class TraficStorageManager(AbstractTraficStorageManager):

    def __init__(self, file_path: str, cache_session: AbstractCacheService):
        self._file_path = file_path
        self.log_to_write = {}
        self._cache_service = cache_session


    def universal_default(self, o):
        if isinstance(o, bytes):
            try:
                return o.decode('utf-8')
            except UnicodeDecodeError:
                return o.hex()
        return str(o)


    def ndjson_write(self, log, year: int, month: int, day: int, hour: int, minute: int):
        path_to_dir = str(year)+"_"+str(month)+"_"+str(day)+"/"

        if not os.path.exists(self._file_path+path_to_dir):
            print("make")
            os.makedirs(self._file_path+path_to_dir) 
        
        if minute <= 30:
            path_file = f"{hour}_30.ndjson" 
        else:
            path_file = f"{hour}_60.ndjson"
        with open(self._file_path+path_to_dir+path_file, "a", encoding="utf-8") as f:
            data = json.dumps(log, default=self.universal_default, ensure_ascii=False)
            f.write(data+"\n")


    def ndjson_read(self, from: datetime, to: Optional[datetime], group_by: str):
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


    def write(self, logs, hour, minute):
        today = datetime.date.today()
        month = today.month  
        day = today.day     
        year = today.year

        self.log_to_write = {}

        num_protocols = {
            "Ether": 0, "IPv4": 0, "TCP": 0, "UDP": 0, "ICMP": 0,
            "IPv6": 0, "ARP": 0, "DNS": 0, "HTTP": 0, "HTTPS": 0,
            "Unknown": 0
        }
        ips_src, ips_dst = {}, {}
        macs_src, macs_dst = {}, {}
        process_names = {}

        for pkt in logs:
            if not isinstance(pkt, dict):
                continue

            # --- Протокол ---
            proto = 'Unknown'
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

            # --- IP ---
            ip_src = pkt.get("ip_src") or pkt.get("ipv6_src")
            ip_dst = pkt.get("ip_dst") or pkt.get("ipv6_dst")

            if ip_src:
                ips_src[ip_src] = ips_src.get(ip_src, 0) + 1
            if ip_dst:
                ips_dst[ip_dst] = ips_dst.get(ip_dst, 0) + 1

            # --- MAC ---
            mac_src = pkt.get("mac_src")
            mac_dst = pkt.get("mac_dst")
            if mac_src:
                macs_src[mac_src] = macs_src.get(mac_src, 0) + 1
            if mac_dst:
                macs_dst[mac_dst] = macs_dst.get(mac_dst, 0) + 1

            # --- Process by port ---
            for port_field, ip_field in [("tcp_sport", "ip_src"), ("udp_sport", "ip_src"),
                                         ("tcp_dport", "ip_dst"), ("udp_dport", "ip_dst")]:
                port = pkt.get(port_field)
                ip = pkt.get(ip_field)
                if port and ip:
                    port_processes = self._cache_service.hgetall(ip)
                    process_name = port_processes.get(str(port))
                    if process_name:
                        process_names[process_name] = process_names.get(process_name, 0) + 1

        self.log_to_write.update({
            "num_proto": num_protocols,
            "ips_src": ips_src,
            "ips_dst": ips_dst,
            "macs_src": macs_src,
            "macs_dst": macs_dst
        })
        self.log_to_write.update(process_names)  
        self.log_to_write.update({"time": logs[0]["time"]})
        self.ndjson_write(
            log=self.log_to_write,
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
        )




