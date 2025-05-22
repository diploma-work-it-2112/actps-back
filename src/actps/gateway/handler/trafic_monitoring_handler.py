import json
import time
import asyncio

from fastapi import WebSocket, WebSocketDisconnect

from src.actps.integrations.redis.redis import RedisCacheService


redis_trafic_monitor_session = RedisCacheService(db=2)



def convert_bytes_to_str(data):
    res = {}
    for key in list(data.keys()):
        res[key.decode("utf-8")] = data[key].decode('utf-8', errors='replace')

    return res


def get_packet_protocols(pkt: dict) -> set:
    protocols = set()
    if any(k.startswith('dns_') for k in pkt):
        protocols.add('DNS')
    if 'http_payload' in pkt or 'http_headers' in pkt:
        protocols.add('HTTP')
    if 'https_payload_hex' in pkt:
        protocols.add('HTTPS')
    if any(k.startswith('icmp_') for k in pkt):
        protocols.add('ICMP')
    if any(k.startswith('tcp_') for k in pkt):
        protocols.add('TCP')
    if any(k.startswith('udp_') for k in pkt):
        protocols.add('UDP')
    if any(k.startswith('ipv6_') for k in pkt):
        protocols.add('IPv6')
    if any(k.startswith('ip_') for k in pkt):
        protocols.add('IPv4')
    if any(k.startswith('arp_') for k in pkt):
        protocols.add('ARP')
    if any(k.startswith('mac_') for k in pkt):
        protocols.add('Ethernet')
    return protocols


async def monitor_trafic_handler(ws: WebSocket, ip: str, protocol: str):
    await ws.accept()
    print("accept")
    try:
        first_id = None
        while True:
            data = redis_trafic_monitor_session.xrange(
                stream_key="trafic_logs_key", min="-", max="+", count=50
            )
            count = 0
            for id, fields in data:
                if count == 0 and first_id == id:
                    break
                elif count == 0:
                    first_id = id
                count += 1

                fields = convert_bytes_to_str(fields)
                try:
                    pkt = fields if isinstance(fields, dict) else json.loads(fields)
                except Exception as e:
                    print("Ошибка парсинга пакета:", e)
                    continue

                if ip.lower() != "all":
                    ip_src = pkt.get("ip_src", "")
                    ip_dst = pkt.get("ip_dst", "")
                    if ip not in [ip_src, ip_dst]:
                        continue

                detected_protocols = get_packet_protocols(pkt)
                if protocol.lower() != "all" and protocol.upper() not in detected_protocols:
                    continue

                json_data = json.dumps(pkt)
                print(json_data)
                await ws.send_text(json_data)
            
            await asyncio.sleep(0.05)
    except WebSocketDisconnect:
        print("Close")
    except Exception as e:
        print("Ошибка в monitor_trafic_handler:", e)
