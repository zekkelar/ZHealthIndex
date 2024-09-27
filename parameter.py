
dissolve_gas_limit = {
	"H2":{
		"low":50,
		"up":150,
		"w":2

	},"CH4":{
		"low":30,
		"up":130,
		"w":3
	},"C2H6":{
		"low":20,
		"up":90,
		"w":3
	},"C2H4":{
		"low":60,
		"up":280,
		"w":3
	},"C2H2":{
		"low":0,
		"up":5,
		"w":5
	},"CO":{
		"low":400,
		"up":600,
		"w":1
	},"CO2":{
		"low":3800,
		"up":14000,
		"w":1
	}
}

oil_quality = {
	"Breakdown Voltage":{
		"low":40,
		"up":60,
		"w":3
	},"Water Content":{
		"low":10,
		"up":30,
		"w":3
	},"Dielectric Loss":{
		"low":0.2,
		"up":4,
		"w":4
	},"Acid Value":{
		"low":0.01,
		"up":4,
		"w":1
	},"Absorption Ratio":{
		"low":1,
		"up":1.5
	},"DC Resistance":{
		"low":1,
		"up":2
	}, "Partial Discharge":{
		"low":50,
		"up":250
	}, "Dielectric Loss Two":{
		"low":0.5,
		"up":2
	}


}
trafo_load_factor_coef = {
		"1":[0,60],
		"1.1":[61, 80],
		"1.25":[81, 100],
		"1.6":[101, 120]
		
}

HI0 = 0.5


trafo_environment_factor_coef = {
	"Heavy":1.15,
	"Light":1.05,
	"Medium":1.1,
	"Very heavy":1.3,
	"Very light":1
}


furfural_status_table = {
	"A":{
		"content":[0, 0.1],
		"index":0
	},"B":{
		"content":[0.1, 0.5],
		"index":2
	},"C":{
		"content":[0.5, 1],
		"index":4
	},"D":{
		"content":[1.0, 5.0],
		"index":6
	},"E":{
		"content":[5, 100],
		"index":8
	}
}


test_item_weight_coefficient_table = {
	"Dissolve Gas":10,
	"Oil Quality Index":8,
	"Furfural":8,
	"Dielectric Loss":5,
	"Absorption Ratio":5,
	"DC Resistance":5,
	"Partial Discharge":10
}


res_hi = {
	'Good':[0, 2],
	'Medium':[2.1, 6],
	'Bad':[6.1, 8],
	'Very Bad':[8.1, 10]
}



zek_oil_quality =dict()
zek_dgi = dict()
zek_h2 = dict()