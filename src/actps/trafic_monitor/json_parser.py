from scapy.all import sniff, Ether, IP, TCP, UDP, ICMP, Raw, ARP, IPv6, DNS, DNSQR
import time

from src.actps.core.trafic_monitor import AbstractTraficParser


class ScapyJSONTraficParse(AbstractTraficParser):

    def parce(self, packet):
        try:
            log_data = {}
            known = False

            if packet.haslayer(Ether):
                log_data.update(self.ether_parse(packet))
                known = True

            if packet.haslayer(IP):
                log_data.update(self.ip_parse(packet))
                known = True

            if packet.haslayer(TCP):
                log_data.update(self.tcp_parse(packet))
                known = True

            elif packet.haslayer(UDP):
                log_data.update(self.udp_parse(packet))
                known = True

            elif packet.haslayer(ICMP):
                log_data.update(self.icmp_parse(packet))
                known = True

            if packet.haslayer(IPv6):
                log_data.update(self.ipv6_parse(packet))
                known = True

            if packet.haslayer(ARP):
                log_data.update(self.arp_parse(packet))
                known = True

            if packet.haslayer(TCP) and packet.haslayer(Raw):
                tcp_layer = packet[TCP]
                if tcp_layer.sport == 80 or tcp_layer.dport == 80:
                    log_data.update(self.http_parse(packet))
                elif tcp_layer.sport == 443 or tcp_layer.dport == 443:
                    log_data.update(self.https_parse(packet))
                known = True

            if packet.haslayer(DNS):
                log_data.update(self.dns_parse(packet))
                known = True

            if not known:
                print(packet)
                log_data["type"] = "unknown"

            log_data["time"] = time.time()
            return log_data
        except Exception as e:
            print("Parse error", e)

    def ether_parse(self, packet) -> dict:
        res = {}
        res['mac_src'] = packet[Ether].src
        res['mac_dst'] = packet[Ether].dst
        res['eth_type'] = hex(packet[Ether].type)
        return res

    def ip_parse(self, packet) -> dict:
        res = {}
        res['ip_src'] = packet[IP].src
        res['ip_dst'] = packet[IP].dst
        res['ip_ttl'] = packet[IP].ttl
        res['ip_proto'] = packet[IP].proto
        if packet[IP].flags:
            res['ip_flags'] = str(packet[IP].flags)
        if packet[IP].options:
            res['ip_options'] = packet[IP].options
        return res

    def tcp_parse(self, packet) -> dict:
        res = {}
        tcp_layer = packet[TCP]
        res['tcp_sport'] = tcp_layer.sport
        res['tcp_dport'] = tcp_layer.dport
        res['tcp_flags'] = str(tcp_layer.flags)
        res['tcp_seq'] = tcp_layer.seq
        res['tcp_ack'] = tcp_layer.ack
        res['tcp_window'] = tcp_layer.window
        res['tcp_payload'] = str(bytes(tcp_layer.payload))
        return res

    def udp_parse(self, packet) -> dict:
        res = {}
        udp_layer = packet[UDP]
        res['udp_sport'] = udp_layer.sport
        res['udp_dport'] = udp_layer.dport
        res['udp_len'] = udp_layer.len
        res['udp_checksum'] = udp_layer.chksum
        res['udp_payload'] = str(bytes(udp_layer.payload))
        return res

    def icmp_parse(self, packet) -> dict:
        res = {}
        icmp_layer = packet[ICMP]
        res['icmp_type'] = icmp_layer.type
        res['icmp_code'] = icmp_layer.code
        res['icmp_checksum'] = icmp_layer.chksum
        res['icmp_payload'] = str(bytes(icmp_layer.payload))
        if icmp_layer.type in [0, 8]:
            res['icmp_id'] = icmp_layer.id
            res['icmp_seq'] = icmp_layer.seq
        return res

    def ipv6_parse(self, packet) -> dict:
        res = {}
        ipv6_layer = packet[IPv6]
        res['ipv6_version'] = ipv6_layer.version
        res['ipv6_traffic_class'] = ipv6_layer.tc
        res['ipv6_flow_label'] = ipv6_layer.fl
        res['ipv6_payload_length'] = ipv6_layer.plen
        res['ipv6_next_header'] = ipv6_layer.nh
        res['ipv6_hop_limit'] = ipv6_layer.hlim
        res['ipv6_src'] = ipv6_layer.src
        res['ipv6_dst'] = ipv6_layer.dst
        return res

    def arp_parse(self, packet) -> dict:
        res = {}
        arp_layer = packet[ARP]
        res['arp_hwtype'] = arp_layer.hwtype
        res['arp_ptype'] = arp_layer.ptype
        res['arp_hwlen'] = arp_layer.hwlen
        res['arp_plen'] = arp_layer.plen
        res['arp_op'] = arp_layer.op
        res['arp_hwsrc'] = arp_layer.hwsrc
        res['arp_psrc'] = arp_layer.psrc
        res['arp_hwdst'] = arp_layer.hwdst
        res['arp_pdst'] = arp_layer.pdst
        return res

    def http_parse(self, packet) -> dict:
        res = {}
        raw_payload = packet[Raw].load
        try:
            http_text = raw_payload.decode('utf-8', errors='replace')
            res['http_payload'] = http_text
            lines = http_text.splitlines()
            if lines:
                res['http_request_line'] = lines[0]
                headers = {}
                for line in lines[1:]:
                    if ": " in line:
                        key, value = line.split(": ", 1)
                        headers[key] = value
                res['http_headers'] = headers
        except Exception as e:
            res['http_payload'] = f"Error decoding HTTP payload: {e}"
        return res

    def https_parse(self, packet) -> dict:
        res = {}
        raw_payload = packet[Raw].load
        res['https_payload_hex'] = raw_payload.hex()
        return res

    def dns_parse(self, packet) -> dict:
        res = {}
        dns_layer = packet[DNS]
        res['dns_id'] = dns_layer.id
        res['dns_qr'] = dns_layer.qr
        res['dns_opcode'] = dns_layer.opcode
        res['dns_aa'] = dns_layer.aa
        res['dns_tc'] = dns_layer.tc
        res['dns_rd'] = dns_layer.rd
        res['dns_ra'] = dns_layer.ra
        res['dns_z'] = dns_layer.z
        res['dns_rcode'] = dns_layer.rcode
        res['dns_qdcount'] = dns_layer.qdcount
        res['dns_ancount'] = dns_layer.ancount
        res['dns_nscount'] = dns_layer.nscount
        res['dns_arcount'] = dns_layer.arcount

        if dns_layer.qdcount > 0 and packet.haslayer(DNSQR):
            dns_qr = packet[DNSQR]
            res['dns_qname'] = dns_qr.qname.decode() if isinstance(dns_qr.qname, bytes) else dns_qr.qname
            res['dns_qtype'] = dns_qr.qtype
            res['dns_qclass'] = dns_qr.qclass

        if dns_layer.ancount > 0:
            answers = []
            # Если количество ответов равно 1, поле an может быть одиночным объектом
            if dns_layer.ancount == 1:
                dns_rr = dns_layer.an
                answer = {
                    'rrname': dns_rr.rrname.decode() if isinstance(dns_rr.rrname, bytes) else dns_rr.rrname,
                    'type': dns_rr.type,
                    'rclass': dns_rr.rclass,
                    'ttl': dns_rr.ttl,
                }
                answers.append(answer)
            else:
                for i in range(dns_layer.ancount):
                    dns_rr = dns_layer.an[i]
                    answer = {
                        'rrname': dns_rr.rrname.decode() if isinstance(dns_rr.rrname, bytes) else dns_rr.rrname,
                        'type': dns_rr.type,
                        'rclass': dns_rr.rclass,
                        'ttl': dns_rr.ttl,
                    }
                    answers.append(answer)
            res['dns_answers'] = answers
        return res
