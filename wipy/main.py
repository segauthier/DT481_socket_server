import pycom
import utime
import ujson
import ustruct

from machine import UART
from lib.box_data_template import *

#l'id de chaque Box doit être unique et  modifié avant de flasher
box_id = 2
BOX_data = {BOX_ID : box_id}
moxbox_stream = {}

# Init UART
uart = UART(1, baudrate=115200,  bits=8, parity=None, stop=1, pins=('P3', 'P4'))

# Init socket
port = 8002
s = usocket.socket()

#state variable
i=0
connected = False

def read_STNUCLEO():
    while(uart.any()<31):
        utime.sleep_ms(10)

    inData = uart.read(uart.any())

    BME680_data[tVOC] = (inData[0] + 256*inData[1])/100
    BME680_data[IAQ_ACC] = inData[2]
    BME680_data[TEMP] = (inData[3] + 256*inData[4])/100
    BME680_data[HUM] = (inData[5] + 256 * inData[6])/100
    #BME680_data[PRES] = (inData[7] + 256 * inData[8])/100
    BME680_data[GAS] = (inData[9] + 256 * inData[10])/100

    SGP30_data[tVOC] = (inData[11] + 256 * inData[12])
    SGP30_data[eCO2] = (inData[13] + 256 * inData[14])

    CCS811_data[eCO2] = (inData[15] + 256 * inData[16])
    CCS811_data[tVOC] = (inData[17] + 256 * inData[18])

    BOX_data[BOX_ID] = box_id

    BOX_data[CO2_ref] = ustruct.unpack('>f', bytearray([inData[19], inData[20], inData[21], inData[22]]))[0]
    BOX_data[T_ref] = ustruct.unpack('>f', bytearray([inData[23], inData[24], inData[25], inData[26]]))[0]
    BOX_data[RH_ref] = ustruct.unpack('>f', bytearray([inData[27], inData[28], inData[29], inData[30]]))[0]

    moxbox_stream[BME680] = BME680_data
    moxbox_stream[SGP30] = SGP30_data
    moxbox_stream[CCS811] = CCS811_data
    moxbox_stream[BOX_params] = BOX_data

def send_socket():
    jdump = ujson.dumps(moxbox_stream)
    try :
        s.write(jdump)
        print(jdump)
        connected = True
    except :
        s.close()
        connected = False
        print("Unable to write on socket")
    finally:
        return connected

while True:
    (year, month, day, hour, minute, seconds, wday, yday) = utime.localtime(utime.time())
    print("Time: ", hour, minute, seconds)

    if not connected:
        try:
            s.connect(usocket.getaddrinfo(hote, port)[0][-1])
            connected = True
            print("Connected to server:",hote,',port:',port)
        except OSError:
            s.close()
            s = usocket.socket()
            utime.sleep_ms(500)
            connected = False
            print("Unable to connect the server:",hote,',port:',port)

    if connected:
        utime.sleep_ms(500)
        read_STNUCLEO()
        connected = send_socket()
        print("Connected : ", connected)
        i=i+1
