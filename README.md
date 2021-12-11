# 1. General
***
EnOcean is battery-less wireless communication standard, which enables to build maintainance-free data aquisition system.
This repository provides python scripts which enable you to receive and view EnOcean telegrams on LinuxOS.

# Target frequencies
***
as you know, EnOcean has 4 radip frequency valiant, 868MHz, 902MHz(U), 928MHz(J), 2.4GHz(Z).
for now (11th Dec 2021), this repository forcus on following valiant.
- 928MHz(J)

# 2. System requirements
***
OS: Ubuntu, Raspbian
Python: 3.7 (or latter)
EnOcean telegram receiver: USB400J *928MHz(J) product series

# 3. Setting
***
firstlly, clone this repositoty into your system, and move to root directory of repository.
to fix USB device name, coppy rules file to "/etc/udev/rules.d/".
```
$ sudo cp ./rules/80-enocean.rules /etc/udev/rules.d/
```
note: if your system already has rules file which prefix is 80, change prefix to not-used number, for ex.,
```
$ sudo cp ./rules/80-enocean.rules /etc/udev/rules.d/79-enocean.rules
```
insert USB40J into USB port, then check recognition on your system with following command.
```
$ ls /dev/ | grep ttyUSB
```
if you find "ttyUSBenocean", it works good.


Next, install requirements
```
$ sudo pip3 install -r requirements.txt
```

# 4. example application: show 928MHz(J) telegram data
***
According to your transmitter device, change description on sensor_info.json in sensor_info directory.
here's example.
```
{
    "0029799d": {
        "name": "switch_1",
        "type": "rocker_switch",
        "place": "room_1",
        "eep": "F6-02-04",
        "comment": "control flor light"
    },
    ...
}
```
"0028e8ce" is ID (hex) of transmitter device, and you need to specify EEP on "eep".
"name", "type", "place" and "comment" shpuld be specified according to your system.
you have to mark all your transmitter device's infomation on this JSON file.
data from the device which is not listed on this file, can't treat this scripts.

corresponding EEPs are following.
- F6_02_04 (rocker switch)
- D5_00_01 (magnet contact sensor)
- A5_02_05 (temperature sensor)
- A5_04_01 (tempearture and humidity sensor)

you can add another EEP, it is required to add corresponding method and function pointer to enocean_equipment_profiles.py 

start app example with
```
$ sudo python3 app_example_receive_data_J.py
```
and transmit telegram (e.g. press switch), then you can see telegram data on console like this. 
```
# rocker switch
{
    'data': {'AI': 0, 'AO': 0, 'BI': 1, 'BO': 0, 'e_bow': 1},
    'eep': 'F6-02-04',
    'name': 'switch_1',
    'orig_id': '0029799d',
    'packet_type': '0x0a',
    'place': 'room_1',
    'recv_at': '2021-12-11 19:51:01',
    'rssi_dbm': -45,
    'sub_tel_num': 1
}

# contact sensor
{
    'data': {'learn': 1, 'state': 'close'},
    'eep': 'D5-00-01',
    'name': 'door_state_refrigerator',
    'orig_id': '04004049',
    'packet_type': '0x0a',
    'place': 'else',
    'recv_at': '2021-12-11 19:53:21',
    'rssi_dbm': -82,
    'sub_tel_num': 1
}

# temperature & humidity sensor
{
    'data': {'avail_temp': 1,
            'humidity_percent': 51.0,
            'learn': 0,
            'temperature_cdeg': 24.5},
    'eep': 'A5-04-01',
    'name': 'temp_humid_01',
    'orig_id': '0400f66b',
    'packet_type': '0x0a',
    'place': '1F_living_room',
    'recv_at': '2021-12-11 19:58:13',
    'rssi_dbm': -55,
    'sub_tel_num': 1
}
```
in this app, data (928MHz telegram) handling instance is generated from EnOcean_J class,
get_packet() method parforms packet analysis and returns extructed data from packet like above.


# 5. exsample application: show ESP3 packet
***
you can view ESP3 packet from receiver device with following steps.
Start app example.
```
$ sudo python3 app_example_view_ESP3_packet_J.py
```
and transmit telegram (e.g. press switch), then you can see telegram data on console like this.
note: all received telegram  
```
# rocker switch
{'data': ['0x20', '0x00', '0x29', '0x79', '0x9d', '0x88', '0xb7'],
 'opdata': ['0x01', '0x34'],
 'packet_type': '0x0a'}

# contact sensor
{'data': ['0x21', '0x04', '0x00', '0x40', '0x49', '0x08', '0xc5'],
 'opdata': ['0x01', '0x50'],
 'packet_type': '0x0a'}

# temperature & humidity sensor
{'data': ['0x22',
          '0x04',
          '0x00',
          '0xf6',
          '0x6b',
          '0x00',
          '0x82',
          '0x9b',
          '0x0a',
          '0xf4'],
 'opdata': ['0x01', '0x3c'],
 'packet_type': '0x0a'}
```

# 6. License
***
Copyright (c) 2021 SAri



