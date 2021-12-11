import serial
import crc8
import copy


class ESP3:
	def __init__(self, dev, b_rate, timeout):
		self.dev = dev
		self.b_rate = b_rate
		self.timeout = timeout
		self._init_params()
		self.list_valid_packets = list()
		self.ser = None
		self._open_port(dev, b_rate, timeout)
		return None
	
	def __del__(self):
		self._close_port()
		return None
		
	def _open_port(self):
		try:
			self.ser = serial.Serial(self.dev, self.b_rate, timeout=timeout)
		except:
			raise Exception(f"ERROR: device {self.dev} can't open! ")
		return None

	def _close_port(self):
		if self.ser:
			self.ser.close()
		return None 
		
	def _init_params(self):
		self.state = "wait0x55"
		self.data_len = 0
		self.opdata_len = 0
		self.packet_type = str()
		self.crc8H = 0
		self.list_data = list()
		self.list_opdata = list()
		self.crc8D = 0
		self.downCount = 0
		self.list_header = list()
		return None
		
	def _conv2strhex(self, list_int):
		list_ret = list()
		for memb in list_int:
			list_ret.append(format(memb, '#04x'))
		return list_ret
	
	def _analize(self):
		while self.ser.inWaiting():
			int_recv = int.from_bytes(self.ser.read(1), "little")
			
			if (self.state == "wait0x55"):
				if (int_recv == 0x55):
					self.state = "header"
					self.downCount = 4		
			elif (self.state == "header"):
				if (self.downCount == 4):
					self.data_len += (int_recv * 0x100)
					self.list_header.append(int_recv)
					self.downCount -= 1
					# print(data_len)
				elif (self.downCount == 3):
					self.data_len += int_recv
					self.list_header.append(int_recv)
					self.downCount -= 1
				elif (self.downCount == 2):
					self.opdata_len += int_recv
					self.list_header.append(int_recv)
					self.downCount -= 1
				elif (self.downCount == 1):
					self.packet_type = int_recv
					self.list_header.append(int_recv)
					self.downCount -= 1
				elif (self.downCount == 0):
					# check crc8H
					crc_culc = crc8.crc8()
					crc_culc.update(bytearray(self.list_header))

					if int_recv == int.from_bytes(crc_culc.digest(), "little"):
						# crc8H OK
						self.crc8H = int_recv				
						self.state = "data"
						self.downCount = self.data_len
					else:
						self._init_params()
						
			elif (self.state == "data"):
				self.list_data.append(int_recv)
				self.downCount -= 1
				if self.downCount == 0:
					self.state = "opdata"
					self.downCount = self.opdata_len
			elif (self.state == "opdata"):
				self.list_opdata.append(int_recv)
				self.downCount -= 1
				if self.downCount == 0:
					self.state = "crc8D_check"
		
			elif (self.state == "crc8D_check"):
				# check crc8H
				crc_culc = crc8.crc8()
				crc_culc.update(bytearray(self.list_data + self.list_opdata))
				if int_recv == int.from_bytes(crc_culc.digest(), "little"):
					# crc8D OK
					self.crc8D = int_recv
					dict_packet = dict()
					dict_packet["data"] = self._conv2strhex(self.list_data)
					dict_packet["opdata"] = self._conv2strhex(self.list_opdata)
					dict_packet["packet_type"] = format(self.packet_type, '#04x')
					self.list_valid_packets.append(copy.deepcopy(dict_packet))
				else:
					pass
				# init params
				self._init_params()
		return None
		
	def get_packet(self):
		self._analize()
		ret = None
		if len(self.list_valid_packets) > 0:
			ret = copy.deepcopy(self.list_valid_packets[0])
			if len(self.list_valid_packets) == 1:
				self.list_valid_packets = list() # init
			else:
				self.list_valid_packets =  self.list_valid_packets[1:]
		return ret
		
	def get_packet_num(self):
		self._analize()
		return len(self.list_valid_packets)
		

def view_packet_loop():
	import time
	print("read ESP3 packets")
	handler = ESP3()
	while True:
		while handler.get_packet_num():
			print(handler.get_packet())
		time.sleep(0.1)


if __name__ == "__main__":
	view_packet_loop()

