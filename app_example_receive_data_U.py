import os
import time
from pprint import pprint
from utils.enocean_driver import EnOcean_U


def view_packet_loop():
    eo = EnOcean_U()
    while True:
        try:
            packet = eo.get_packet()
            if packet:
                print("\n")
                pprint(packet)
        except Exception as e:
            print(e)
        time.sleep(0.3)
    return None


if __name__ == "__main__":
    view_packet_loop()

    