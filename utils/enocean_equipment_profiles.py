# rocker switch -------------------
def F6_02_04(list_data):
    # exception handler -----------
    if len(list_data) != 1:
        print("data length doesn't match specified EEP.")
        return None
    # data derivation -------------
    int_data = int(list_data[0], 0)
    dict_ret = dict()
    dict_ret["e_bow"] = int(0)
    dict_ret["BI"] = int(0)
    dict_ret["BO"] = int(0)
    dict_ret["AI"] = int(0)
    dict_ret["AO"] = int(0)
    if 0b10000000 & int_data:
        dict_ret["e_bow"] = int(1)
    if 0b00001000 & int_data:
        dict_ret["BI"] = int(1)
    if 0b00000100 & int_data:
        dict_ret["BO"] = int(1)
    if 0b00000010 & int_data:
        dict_ret["AI"] = int(1)
    if 0b00000001 & int_data:
        dict_ret["AO"] = int(1)
    return dict_ret


# magnet contact sensor ------------
def D5_00_01(list_data):
    # exception handler ------------
    if len(list_data) != 1:
        print("data length doesn't match specified EEP.")
        return None
    # data derivation -------------
    int_data = int(list_data[0], 0)
    dict_ret = dict()
    dict_ret["state"] = "open"
    dict_ret["learn"] = int(0)
    if 0b00000001 & int_data:
        dict_ret["state"] = "close"
    if 0b00001000 & int_data:
        dict_ret["learn"] = int(1)
    return dict_ret


# temperature sensor ----------------
def A5_02_05(list_data):
    round_num = 1
    # exception handler ------------
    if len(list_data) != 4:
        print("data length doesn't match specified EEP.")
        return None
    # data derivation -------------
    int_data_0 = int(list_data[-1], 0)
    int_data_1 = int(list_data[-2], 0)
    dict_ret = dict()
    dict_ret["temperature_cdeg"] = None
    dict_ret["learn"] = int(0)
    dict_ret["temperature_cdeg"] = round((0xFF - int_data_1) * 40 / 255, round_num)
    if 0b00001000 & int_data_0:
        dict_ret["learn"] = int(1)
    return dict_ret


# tempearture and humidity sensor ---------------
def A5_04_01(list_data):
    round_num_temp = 1
    round_num_humid = 1
    # exception handler ------------
    if len(list_data) != 4:
        print("data length doesn't match specified EEP.")
        return None
    # data derivation -------------
    dict_ret = dict()
    # humidity ---
    int_data_2 = int(list_data[1], 0)
    dict_ret["humidity_percent"] = round((int_data_2 * 100 / 255), round_num_humid)
    # temperature ---
    int_data_1 = int(list_data[2], 0)
    dict_ret["temperature_cdeg"] = round((int_data_1 * 40 / 255), round_num_temp)
    # misc ---
    dict_ret["learn"] = int(0)
    dict_ret["avail_temp"] = int(0)
    int_data_0 = int(list_data[3], 0)
    if not 0b00001000 & int_data_0:
        dict_ret["learn"] = int(1) # teach-in
    if 0b00000010 & int_data_0:
        dict_ret["avail_temp"] = int(1) # temperature sensor available
    return dict_ret


# function pointer -----------------------
eep_get_data = {
    "F6-02-04": F6_02_04,
    "D5-00-01": D5_00_01,
    "A5-02-05": A5_02_05,
    "A5-04-01": A5_04_01,
}