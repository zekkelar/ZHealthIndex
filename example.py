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

from ZHealthIndex import (Theoritical_health_index,
						  LastCalculate, dissolved_gas,FurfuralIndex)

def test_health_index_():
	df = pd.read_excel('dataset.xlsx')
	df.columns = df.columns.str.strip()
	#ini for i in range ini krna di excel ku rownya ada 3, sbnrnya 3 bisa diganti jadi panjang dari df.column (opsional aja lah, intinya nyesuain brp isinya)
	for i in range(0, len(df)): # len(df) itu panjang barisnya

		# wajib, mendefinisikan Class ini
		LastCalculation = LastCalculate()
		Initial_DG = dissolved_gas()
		run = Theoritical_health_index(age=df['Age'].tolist()[i], load_rate=df['Load Rate'].tolist()[i], polution_level=df['Polution Level'].tolist()[i])

		# mencari H1
		THI = run.main()
		"""
		`` to show environment factor is ``
		print(THI['H1']) # ini untuk H1
		print(THI['FE']) # ini untuk Fe
		print(THI['FL']) # ini untuk FL
		"""

		"""
		ini semua hukumnya wajib, samain aja kayak begini formatnya klo mau aman
		"""
		h2 = Initial_DG.accending_func(value=df['H2'].tolist()[i], parameter=dissolve_gas_limit["H2"])
		ch4 = Initial_DG.accending_func(value=df['CH4'].tolist()[i], parameter=dissolve_gas_limit["CH4"])
		c2h6 = Initial_DG.accending_func(value=df['C2H6'].tolist()[i], parameter=dissolve_gas_limit["C2H6"])
		c2h4 = Initial_DG.accending_func(value=df['C2H4'].tolist()[i], parameter=dissolve_gas_limit["C2H4"])
		c2h2 = Initial_DG.accending_func(value=df['C2H2'].tolist()[i], parameter=dissolve_gas_limit["C2H2"])
		co = Initial_DG.accending_func(value=df['CO'].tolist()[i], parameter=dissolve_gas_limit["CO"])
		co2 = Initial_DG.accending_func(value=df['CO2'].tolist()[i], parameter=parameter.dissolve_gas_limit["CO2"])
		zek_dgi['H2'] = h2
		zek_dgi['CH4'] = ch4 
		zek_dgi['C2H6'] = c2h6
		zek_dgi['C2H4'] = c2h4
		zek_dgi['C2H2'] = c2h2
		zek_dgi['CO'] = co 
		zek_dgi['CO2'] = co2 

		# untuk memunculkan berapa DGI nya, tinggal print(dgi)
		dgi = Initial_DG.DGI(dissolved_gas=zek_dgi)



		BV = Initial_DG.descending_func(value=df['Breakdown Voltage'].tolist()[i], parameter=oil_quality["Breakdown Voltage"])
		WC = Initial_DG.accending_func(value=df['Water Content'].tolist()[i], parameter=oil_quality["Water Content"])
		DL = Initial_DG.accending_func(value=df['Dielectric Loss'].tolist()[i], parameter=oil_quality["Dielectric Loss"])
		AV = Initial_DG.accending_func(value=df['Acid Value'].tolist()[i], parameter=oil_quality["Acid Value"])
		zek_oil_quality['Breakdown Voltage'] = BV 
		zek_oil_quality['Water Content'] = WC 
		zek_oil_quality['Dielectric Loss'] = DL 
		zek_oil_quality['Acid Value'] = AV
		oil_quality_index = Initial_DG.OQI(zek_oil_quality)


		runf = FurfuralIndex(df['CO2'].tolist()[i], df['CO'].tolist()[i])
		furfural = runf.detect_furfural(runf.main())

		DLONE = Initial_DG.accending_func(value=df['Dielectric Loss Two'].tolist()[i], parameter=parameter.oil_quality["Dielectric Loss Two"])
		DCR = Initial_DG.accending_func(value=df['DC Resistance'].tolist()[i], parameter=parameter.oil_quality["DC Resistance"])
		PD = Initial_DG.accending_func(value=df['Partial Discharge'].tolist()[0], parameter=oil_quality["Partial Discharge"])
		AR = Initial_DG.descending_func(value=df['Absorption Ratio'].tolist()[i], parameter=oil_quality["Absorption Ratio"])
		zek_h2['Furfural'] = furfural
		zek_h2['Dielectric Loss'] = DLONE
		zek_h2['Absorption Ratio'] = AR 
		zek_h2['DC Resistance'] = DCR
		zek_h2['Partial Discharge'] = PD 
		zek_h2['Oil Quality Index'] = oil_quality_index
		zek_h2['Dissolve Gas'] = dgi

		H2 = (LastCalculation.H2(zek_h2))
		HI = (LastCalculation.HI(THI['HI1'], H2))
		statusHI = LastCalculation.Status(HI)
		print(f'Row Number : {i}')
		print(f'H2 : {H2}')
		print(f'HI : {HI}')
		print('')

if __name__ == "__main__":
	test_health_index_()
