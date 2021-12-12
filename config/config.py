class Common():
    SERIAL_DEVICE = "/dev/ttyUSBenocean"
    TIMEOUT = 0.1
    FLUG_USE_0x = False


class J(Common):
    BAUDRATE = 57600
    SENSOR_INFO_PATH = "./sensor_info/sensor_info_J.json"


class U(Common):
    BAUDRATE = 57600
    SENSOR_INFO_PATH = "./sensor_info/sensor_info_U.json"
