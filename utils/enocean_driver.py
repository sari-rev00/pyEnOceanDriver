import json
from datetime import datetime

from utils.enocean_serial_protocol import ESP3
from utils.enocean_radio_protocol import ERP2
from utils.enocean_equipment_profiles import eep_get_data
from config.config import J


class EnOcean_J:
    def __init__(
            self, 
            sensor_info_path=J.SENSOR_INFO_PATH, 
            dev=J.SERIAL_DEVICE, 
            b_rate=J.BAUDRATE, 
            timeout=J.TIMEOUT):
        self.esp3 = ESP3(dev=dev, b_rate=b_rate, timeout=timeout)
        self.erp2 = ERP2()
        self.sensor_info = self._conv_dict_keys_str2int(
            self._load_sensor_info(sensor_info_path))
        return None
        
    def _load_sensor_info(self, path):
        with open(path, "r") as f:
            ret = json.load(f)
        return ret
    
    def _id_conv2num(self, list_id):
        ret = int(0)
        num = len(list_id) - 1
        for b in list_id:
            ret += int(b, 0) * 0x100 ** num
            num -= 1
        return ret
    
    def _conv_dict_keys_str2int(self, d):
        dict_ret = dict()
        for key in d.keys():
            int_key = int(("0x" + key), 0)
            dict_ret[int_key] = d[key]
        return dict_ret
    
    def get_packet(self):
        if self.esp3.get_packet_num():
            dict_esp3_proc = self.esp3.get_packet()
            dict_erp2_proc = self.erp2.get_dict_data(dict_esp3_proc["data"])
            orig_id = self._id_conv2num(dict_erp2_proc["orig_id"])
            try:
                eep = self.sensor_info[orig_id]["eep"]
                name = self.sensor_info[orig_id]["name"]
                place = self.sensor_info[orig_id]["place"]
            except:
                print("error: orig_id not registered")
                return None
            dict_data = eep_get_data[eep](dict_erp2_proc["data"])
            rssi = int(dict_esp3_proc["opdata"][1], 0) * -1
            sub_tel_num = int(dict_esp3_proc["opdata"][0], 0)
            
            ret = dict()
            ret["recv_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if J.FLUG_USE_0x:
                ret["orig_id"] = format(orig_id, "#010x")
            else:
                ret["orig_id"] = format(orig_id, "08x")
            ret["packet_type"] = dict_esp3_proc["packet_type"]
            ret["data"] = dict_data
            ret["rssi_dbm"] = rssi
            ret["sub_tel_num"] = sub_tel_num
            ret["eep"] = eep
            ret["name"] = name
            ret["place"] = place
        else:
            ret = None
        return ret
