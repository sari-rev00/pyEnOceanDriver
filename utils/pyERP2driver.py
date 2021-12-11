class ERP2:
	def __init__(self):
		self._init_params()
		return None
		
	def _init_params(self):
		self.len_header = int(1)
		self.len_ori_id = int(0)
		self.len_dist_id = int(0)
		self.len_ext_head = int(0)
		self.len_ext_type = int(0)
		self.len_data = int(0)
		self.tel_type = str()
		return None
		
	def _check_header(self, header):
		# check address control ================
		add_cnt = int(header, 0) & 0b11100000
		if add_cnt == 0b00000000:
			self.len_ori_id = int(3)
			self.len_dist_id = int(0)
		elif add_cnt == 0b00100000:
			self.len_ori_id = int(4)
			self.len_dist_id = int(0)
		elif add_cnt == 0b01000000:
			self.len_ori_id = int(4)
			self.len_dist_id = int(4)
		elif add_cnt == 0b01100000:
			self.len_ori_id = int(6)
			self.len_dist_id = int(0)
		else:
			pass
		# check extended header availability ===
		ext_head = int(header, 0) & 0b00010000
		if ext_head == 0b00010000:
			self.len_ext_head = int(1)
		else:
			pass
		# check telegram type===================
		tt = int(header, 0) & 0b00001111
		if tt == 0b00000000:
			self.tel_type = "RPS"
			self.len_data = int(1)
		elif tt == 0b00000001:
			self.tel_type = "1BS"
			self.len_data = int(1)
		elif tt == 0b00000010:
			self.tel_type = "4BS"
			self.len_data = int(4)
		elif tt == 0b00001111:
			self.tel_type = "Ext_tel_type"
			self.len_ext_type = int(1)
		else:
			self.tel_type = "else"
		return None

	def _get_orig_id(self, list_data):
		offset_orig_id = (
			self.len_header + 
			self.len_ext_head + 
			self.len_ext_type
		)
		return list_data[offset_orig_id : offset_orig_id + self.len_ori_id]
		
	def _get_data(self, list_data):
		offset_data = (
			self.len_header + 
			self.len_ext_head + 
			self.len_ext_type +
			self.len_ori_id
		)
		return list_data[offset_data : offset_data + self.len_data]
		
	def get_dict_data(self, data):
		dict_ret = dict()
		self._init_params()
		self._check_header(header=data[0])
		dict_ret["tel_type"] = self.tel_type
		dict_ret["orig_id"] = self._get_orig_id(list_data=data)
		dict_ret["data"] = self._get_data(list_data=data)		
		return dict_ret


if __name__ == "__main__":
	sample_data = ['0x20', '0x00', '0x28', '0xe8', '0xce', '0x85', '0x73']
	handler = ERP2()
	print(handler.get_dict_data(sample_data))

	

