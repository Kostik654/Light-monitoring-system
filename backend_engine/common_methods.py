import hashlib
import random
import time

from port_item import PortItem
from logger import LogItOut


def generate_call_id():
    # Call-ID for SIP
    hostname = "monitoring-system.local"  # домен
    return f"{random.randint(100000, 999999)}@{hostname}"

def generate_tag():
    # Tag for SIP
    return hashlib.md5(str(random.randint(100000, 999999)).encode()).hexdigest()

def generate_cseq():
    # CSeq for SIP
    return random.randint(1, 10000)

def generate_branch():
    # Branch for SIP
    return f"z9hG4bK-{hashlib.md5(str(time.time()).encode()).hexdigest()}"



def GetExpectedCodes(codes: str, splitter: str = '-') -> list[int] or None:
    if not codes.__eq__('*'):
        try:
            return list(map(int, codes.split(splitter)))
        except Exception as e:
            LogItOut(message_=f'Expected codes adding error to job: {e}',
                     for_tg=False,
                     add_timestamp=False)
            return None
    else:
        return None


def GetPortsArray(ports_str: str) -> list[PortItem] or None:

    if ports_str.__eq__('*'):
        return None

    ports_: list[PortItem] = []

    # 1234:PortName:100-111,...
    # 1234:PortName:*,...
    try:
        for item in ports_str.split(','):

            item_splitted = item.split(':')
            port_v: int = int(item_splitted[0])
            serv_name: str = item_splitted[1]

            # codes or *
            exc_cds: list[int] = GetExpectedCodes(item_splitted[2])

            ports_.append(PortItem(port_v, serv_name, exc_cds))
    except Exception as e:
        ports_ = None
        LogItOut(message_=f'Ports adding error to SOCKET job: {e}',
                 for_tg=False,
                 add_timestamp=False)
    finally:
        return ports_


def toFixed(num, digits=0) -> str:
    return f"{num:.{digits}f}"