import os
import time
from pprint import pprint
from utils.pyEnOceanDriver import EnOcean
from config.config import Config


def view_packet_loop():
    eo = EnOcean()
    while True:
        try:
            packet = eo.get_packet()
            if packet:
                pprint(packet)
        except Exception as e:
            print(e)
        time.sleep(0.3)
    return None


if __name__ == "__main__":
    view_packet_loop()

    