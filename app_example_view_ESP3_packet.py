import time
from pprint import pprint

from utils.enocean_serial_protocol import ESP3
from config.config import J


COUNT_MAX = 1000
LOOP_WAIT = 0.3

def view_ESP3_packet_loop(conf):
    print("view ESP3 packets")
    handler = ESP3(dev=conf.SERIAL_DEVICE, b_rate=conf.BAUDRATE, timeout=conf.TIMEOUT)
    count = int(0)
    while True:
        while handler.get_packet_num():
            print(f"\n{count}")
            pprint(handler.get_packet())
            count += int(1)
        if count > COUNT_MAX:
            count = int(0)
        time.sleep(LOOP_WAIT)
    return None


if __name__ == "__main__":
    view_ESP3_packet_loop(conf=J)