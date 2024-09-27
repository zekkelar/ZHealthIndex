import parameter, math
import pandas as pd
import numpy as np

from parameter import (dissolve_gas_limit, 
						oil_quality,trafo_load_factor_coef, 
						trafo_environment_factor_coef,
						furfural_status_table,
						test_item_weight_coefficient_table,
						res_hi,
						zek_oil_quality, zek_dgi, zek_h2)

"""
__Library__Name : Health Index Trafo finder
__Coder : Zekkel AR 
"""


class Theoritical_health_index(object):
	"""
	```theoritical health index __class__: berfungsi untuk mencari H1
	disamping itu, ini bisa buat nyari FL, FE, H1
	cara penggunaan
	Theoritical_health_index(age=value, load_rate=value)
	example:
		Theoritical_health_index(age=3, load_rate=60).main()

	output:
		akan mengembalikan langsung nilai H1
	"""
	def __init__(self, age=None, load_rate=None, polution_level=None):
		# menghitung aging
		self.B = ((math.log(10)/math.log(0.5)/(age)))
		self.FL = ""
		self.FE = ""
		self.T = age
		self.HI0 = parameter.HI0
		self.load_rate = load_rate
		self.polution_level=polution_level

	# mencari FL
	def findFL(self):
		#print("loadrate: "+str(self.load_rate))
		for key, value in parameter.trafo_load_factor_coef.items():
			"""
				```unpack value and key from trafo_load_factor_coefficient```
				output from findValue: 
					[61, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
				mencari nilai si loadrate didalem trafo coefficient , sama seperti fungsi LOOKUP di excel
			"""

			findValue = [i if str(self.load_rate) == str(i) else None for i in range(value[0], value[1]+1)]
			
			# ini karena ada nilai None di output, None nya diapus untuk agar bisa digaskan untuk proses selanjutnya
			array2 = list(filter(lambda x: x is not None, findValue))

			#ketika array2, alias output nya ketemu, break looping
			if len(array2)>0:
				return float(key)
				break 

	# find FE
	def findFE(self):
		# just dump dictionary key with polution level
		# sejujurnya ini gampang aja keliatan make mata
		return (parameter.trafo_environment_factor_coef[self.polution_level])

	def findH1(self):
		# makek rumus yang ini: HI0 * e^B*FL*FE*T
		asede = self.HI0 * math.exp(self.B * self.FL * self.FE * self.T)
		return asede

	def main(self):
		Coef = dict()						
		self.FL = float((self.findFL()))
		self.FE = float(self.findFE())
		self.HI1 = float(self.findH1())
		Coef['FL'] =  self.FL 
		Coef['FE'] = self.FE 
		Coef['HI1'] = self.HI1
		Coef['T'] = self.T
		Coef['HI0'] = self.HI0
		"""
		print(f'FL : {self.FL}')
		print(f'FE : {self.FE}')
		print(f'T : {self.T}')
		print(f'HI0 : {self.HI0}')
		print(f"HI1 : {self.HI1}")
		"""
		return Coef


class dissolved_gas:
	def __init__(self):
		pass 

	def accending_func(self, value=None, parameter=None):
		#print(f'Value :{value}| Low : {parameter_low} | Up : {parameter_up}')
		if 0 <= value < parameter['low']:
			return 0
		if parameter['low'] <= value <= parameter['up']:
			calc = 5 + 5 * math.sin(math.pi/(parameter['up'] - parameter['low'])*(value-(parameter['up']+parameter['low'])/2))
			return calc
		if parameter['up'] < value:
			return 10


	def descending_func(self, value=None, parameter=None):
		if parameter==None :assert "Parameter should'nt None, Input your parameter, descending_func(value=value, parameter=your_parameter)"
		if 0 <= value < parameter['low']:
			return 10
		if parameter['low'] <= value <= parameter['up']:
			calc = 5 - 5 * math.sin(math.pi/(parameter['up'] - parameter['low'])*(value-(parameter['up']+parameter['low'])/2))
			return calc 

		if parameter['up'] < value:
			return 0



	def DGI(self, dissolved_gas=None):
		# dissolved_gas = result dari accending function
		calc = 0
		sum_weight = 0

		# parameter gaboleh kurang dari 7, harus complete sesuai dari parameter dari literatur (aslinya walau kurang ttp jalan sih)
		if len(dissolved_gas)<7:assert("Error, DGI Parameter tidak terisi semua: H2, CH4, C2H6, C2H4, C2H2, CO, CO2")

		for all_dir in dissolved_gas:
			calc += (dissolve_gas_limit[all_dir]['w']*dissolved_gas[all_dir])
		for key,value in dissolve_gas_limit.items():
			try:
				sum_weight += value['w']
			except:
				pass 
		return (calc/sum_weight) 

	def OQI(self, oil_quality):
		# 
		calc = 0
		sum_weight = 0
		for oil_val in oil_quality:
			calc += (parameter.oil_quality[oil_val]['w'])*(oil_quality[oil_val])
			

		for key, value in parameter.oil_quality.items():
			try:
				sum_weight += value['w']
			except:
				pass
		return (calc/sum_weight)

class FurfuralIndex:
	def __init__(self, CO2, CO):
		self.CO2 = CO2 
		self.CO = CO 

	def detect_furfural(self, furfural):
		# mengembalikan nilai index furfural berdasarkan kelas
		return parameter.furfural_status_table[furfural]['index']

	def main(self):
		# ini mas yang kemarin di kertas
		# bisa cek kertas bang slamet aja gmn flownya :D
		CO2CO = float(self.CO2)/float(self.CO)
		if float(self.CO)>500:
			if(CO2CO>7):
				return "C"
			if(CO2CO==6):
				return "D"
			if(CO2CO<5):
				return "E"
		else:
			if float(self.CO)<350:
				return "A"
			else:
				return "B"


class LastCalculate:
	def __init__(self):
		pass 

	def HI(self, H1, H2):
		return H1*0.4+H2*0.6

	def Status(self, HI):
		for value, key in parameter.res_hi.items():
			if key[0]<=HI<=key[1]:
				return value
				break

	def H2(self, test_health_index):
		calc = 0
		sum_weight = 0
		for THI in test_health_index:
			calc += parameter.test_item_weight_coefficient_table[THI] * test_health_index[THI]

		for key, value in parameter.test_item_weight_coefficient_table.items():
			sum_weight += value
		return calc/sum_weight

