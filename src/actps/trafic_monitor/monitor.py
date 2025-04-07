from scapy.all import sniff, Ether, IP, TCP, UDP, ICMP, Raw, ARP, IPv6, DNS, DNSQR
import time

from src.actps.core.trafic_monitor import AbstractTraficMonitoring


class TraficMonitor(AbstractTraficMonitoring):

    def __init__(self, log_writer, log_parser):
        self.logs = []
        self.log_writer = log_writer
        self.log_parser = log_parser

    def parce_package(self, packet):
        log_data = {}

        if packet.haslayer(Ether):
            log_data['mac_src'] = packet[Ether].src
            log_data['mac_dst'] = packet[Ether].dst
            log_data['eth_type'] = hex(packet[Ether].type)

        if packet.haslayer(IP):
            log_data['ip_src'] = packet[IP].src
            log_data['ip_dst'] = packet[IP].dst
            log_data['ttl'] = packet[IP].ttl
            log_data['ip_proto'] = packet[IP].proto
            log_data["flags"] = packet[IP].flags
            log_data["options"] = packet[IP].options

        if packet.haslayer(TCP):
            log_data['tcp_sport'] = packet[TCP].sport
            log_data['tcp_dport'] = packet[TCP].dport
            log_data['tcp_flags'] = str(packet[TCP].flags) 
            log_data['tcp_seq'] = packet[TCP].seq
            log_data['tcp_ack'] = packet[TCP].ack
            log_data['tcp_window'] = packet[TCP].window
            log_data['tcp_payload'] = str(bytes(packet[TCP].payload))

        elif packet.haslayer(UDP):
            log_data['udp_sport'] = packet[UDP].sport
            log_data['udp_dport'] = packet[UDP].dport
            log_data['udp_len'] = packet[UDP].len
            log_data['udp_checksum'] = packet[UDP].chksum
            log_data["udp_payload"] = str(bytes(packet[UDP].payload))

        elif packet.haslayer(ICMP):
            icmp_layer = packet[ICMP]
            log_data['icmp_type'] = icmp_layer.type
            log_data['icmp_code'] = icmp_layer.code
            log_data['icmp_checksum'] = icmp_layer.chksum
            log_data["icmp_payload"] = str(bytes(packet[ICMP].payload))
            if icmp_layer.type in [0, 8]:
                log_data['icmp_id'] = icmp_layer.id
                log_data['icmp_seq'] = icmp_layer.seq

        if packet.haslayer(IPv6):
            ipv6_layer = packet[IPv6]
            log_data['ipv6_version'] = ipv6_layer.version
            log_data['ipv6_traffic_class'] = ipv6_layer.tc
            log_data['ipv6_flow_label'] = ipv6_layer.fl 
            log_data['ipv6_payload_length'] = ipv6_layer.plen
            log_data['ipv6_next_header'] = ipv6_layer.nh
            log_data['ipv6_hop_limit'] = ipv6_layer.hlim
            log_data['ipv6_src'] = ipv6_layer.src
            log_data['ipv6_dst'] = ipv6_layer.dst

        if packet.haslayer(ARP):
            arp_layer = packet[ARP]
            log_data['arp_hwtype'] = arp_layer.hwtype
            log_data['arp_ptype'] = arp_layer.ptype
            log_data['arp_hwlen'] = arp_layer.hwlen
            log_data['arp_plen'] = arp_layer.plen
            log_data['arp_op'] = arp_layer.op
            log_data['arp_hwsrc'] = arp_layer.hwsrc
            log_data['arp_psrc'] = arp_layer.psrc
            log_data['arp_hwdst'] = arp_layer.hwdst
            log_data['arp_pdst'] = arp_layer.pdst
            print("ARP Packet:")
            arp_layer.show()

        if packet.haslayer(TCP) and packet.haslayer(Raw):
            raw_payload = packet[Raw].load
            if packet[TCP].sport == 80 or packet[TCP].dport == 80:
                try:
                    http_text = raw_payload.decode('utf-8', errors='replace')
                    log_data['http_payload'] = http_text
                    lines = http_text.splitlines()
                    if lines:
                        log_data['http_request_line'] = lines[0]
                        headers = {}
                        for line in lines[1:]:
                            if ": " in line:
                                key, value = line.split(": ", 1)
                                headers[key] = value
                        log_data['http_headers'] = headers
                except Exception as e:
                    log_data['http_payload'] = f"Error decoding HTTP payload: {e}"
            elif packet[TCP].sport == 443 or packet[TCP].dport == 443:
                log_data['https_payload_hex'] = raw_payload.hex()

        if packet.haslayer(DNS):
            dns_layer = packet[DNS]
            log_data['dns_id'] = dns_layer.id
            log_data['dns_qr'] = dns_layer.qr
            log_data['dns_opcode'] = dns_layer.opcode
            log_data['dns_aa'] = dns_layer.aa
            log_data['dns_tc'] = dns_layer.tc
            log_data['dns_rd'] = dns_layer.rd
            log_data['dns_ra'] = dns_layer.ra
            log_data['dns_z'] = dns_layer.z
            log_data['dns_rcode'] = dns_layer.rcode
            log_data['dns_qdcount'] = dns_layer.qdcount
            log_data['dns_ancount'] = dns_layer.ancount
            log_data['dns_nscount'] = dns_layer.nscount
            log_data['dns_arcount'] = dns_layer.arcount

            if dns_layer.qdcount > 0 and packet.haslayer(DNSQR):
                dns_qr = packet[DNSQR]
                log_data['dns_qname'] = dns_qr.qname.decode() if isinstance(dns_qr.qname, bytes) else dns_qr.qname
                log_data['dns_qtype'] = dns_qr.qtype
                log_data['dns_qclass'] = dns_qr.qclass  

            if dns_layer.ancount > 0:
                answers = []
                for i in range(dns_layer.ancount):
                    dns_rr = dns_layer.an[i]
                    answer = {}
                    answer['rrname'] = dns_rr.rrname.decode() if isinstance(dns_rr.rrname, bytes) else dns_rr.rrname
                    answer['type'] = dns_rr.type                    
                    answer['rclass'] = dns_rr.rclass
                    answer['ttl'] = dns_rr.ttl
                    answer['rdata'] = dns_rr.rdata
                    answers.append(answer)
                log_data['dns_answers'] = answers

        log_data["time"] = time.time()

        return log_data

    def monitor(self, packet):
        log = self.parce_package(packet)
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
