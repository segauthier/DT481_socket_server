
BOX_params = "box_params"
BME680 = "bme680"
SGP30 = "sgp30"
CCS811 = "ccs811"

INDEX = "index"
TIME = "timestamp"
CO2_ref = "CO2_ref"
T_ref = "temperature_ref"
RH_ref = "humidity_ref"

BOX_ID = "box_id"
IAQ = "iaq"
IAQ_ACC = "iaq_acc"
TEMP = "temperature"
HUM = "humidity"
PRES = "pressure"
GAS = "gas"
tVOC = "tVOC"
eCO2 = "eCO2"
CO2 = "CO2"

BOX_data = {BOX_ID: 0, CO2_ref: 0, T_ref: 0, RH_ref: 0}
BME680_data = {tVOC: 0, IAQ_ACC: 0, TEMP: 0, HUM: 0, GAS: 0}
SGP30_data = {tVOC: 0, eCO2: 0}
CCS811_data = {tVOC: 0, eCO2: 0}

moxbox_stream = {BOX_params: BOX_data, BME680: BME680_data, SGP30: SGP30_data, CCS811: CCS811_data}
