from machine import Pin,I2C,PWM
from umqtt.simple import MQTTClient
import time
import network
import machine
import ubinascii
import ujson
import initialise as init

dCycleX = 60
dCycleY = 60
dCycleStep = 5
HEAT_MAP_SIZE = 5          # Maximum iteration times , (HEAT_MAP_SIZE)^2 = how big the heat map is
TEMP_SAMPLE_SIZE=4         # Sample size of the temperature data to obtain a more accurate mean

#Initialise angle as 0 -> duty(30) and Pin allocation
servoX = PWM(Pin(15), freq=50, duty=dCycleX)
servoY = PWM(Pin(13), freq=50, duty=dCycleY)

# data transformation from raw data across I2C bus into desired temperature information
# data transformed according to TMP 007 datasheet -> http://www.ti.com/lit/ds/symlink/tmp007.pdf
def getRawTemperatureData():
    sum_tmp=0
    i2c = I2C(scl=Pin(5),sda=Pin(4),freq=100000)
    for k in range(0,TEMP_SAMPLE_SIZE):
         temperature_reading = i2c.readfrom_mem(64,3,2)
         byteHex = ubinascii.hexlify(bytearray(temperature_reading))
         stringHex = byteHex.decode('ascii')
         hex_int = int(stringHex, 16)
         sum_tmp = sum_tmp + (hex_int >> 2) * 0.03125
         time.sleep(0.3)
    mean_temp = sum_tmp / TEMP_SAMPLE_SIZE
    time.sleep(0.5)
    print ("the mean data is ", mean_temp)
    return mean_temp

# converts raw temperature values into their RGB equivalent, changes according to quantization range
def rawTemperatureDataToRGBHeatMap(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    time.sleep(0.5)
    return r, g, b


# this is how the final JSON output looks like
# {"time" : "2017-2-14 18:56:30", "meanTemperature" : "[[43.35156, 43.375, 44.4375, 45.61719, 46.42188, 47.29688, 47.91406], [46.88282, 44.24219, 42.6875, 41.73438, 41.26563, 41.32813, 42.24219], [42.14063, 39.65625, 38.39063, 37.96875, 37.90625, 38.1875, 38.67188], [38.72656, 36.9375, 35.97656, 35.51563, 35.28125, 35.64063, 35.91406], [35.4375, 34.24219, 33.15625, 32.63281, 32.4375, 32.57813, 33.00781], [33.53125, 32.73438, 32.32031, 31.95313, 31.90625, 31.53906, 31.35937], [31.41406, 31.15625, 31.07813, 31.1875, 31.35937, 31.46875, 31.60156]]", "rgb" : "[[[0, 239, 16], [0, 239, 16], [0, 250, 5], [6, 249, 0], [14, 241, 0], [23, 232, 0], [29, 226, 0]], [[19, 236, 0], [0, 248, 7], [0, 232, 23], [0, 222, 33], [0, 217, 38], [0, 218, 37], [0, 227, 28]], [[0, 226, 29], [0, 201, 54], [0, 188, 67], [0, 184, 71], [0, 183, 72], [0, 186, 69], [0, 191, 64]], [[0, 192, 63], [0, 173, 82], [0, 163, 92], [0, 159, 96], [0, 156, 99], [0, 160, 95], [0, 163, 92]], [[0, 158, 97], [0, 146, 109], [0, 135, 120], [0, 129, 126], [0, 127, 128], [0, 129, 126], [0, 133, 122]], [[0, 139, 116], [0, 130, 125], [0, 126, 129], [0, 122, 133], [0, 122, 133], [0, 118, 137], [0, 116, 139]], [[0, 117, 138], [0, 114, 141], [0, 113, 142], [0, 115, 140], [0, 116, 139], [0, 117, 138], [0, 119, 136]]]"}

def dataToJSON(currentTime,temperatureData,rgbData):

    formatTime = str(currentTime[0]) + '-' + str(currentTime[1]) + '-' + str(currentTime[2]) + ' ' + str(currentTime[4]) + ':' + str(currentTime[5]) + ':' + str(currentTime[6])
    time = '{"time" : ' + '"' + formatTime + '"' + ', '
    temperature = '"temperature" : ' + '"' + str(temperatureData) + '"' + ', '
    rgb = '"rgb" : ' + '"' + str(rgbData) + '"' + '}'
    jsonString = time + temperature + rgb

    return jsonString

def sendDataToMQTTBroker(client,jsonData):
    client.publish("embedTrio/sourceData",bytes(jsonData,"utf-8"))
    print("sent data to MQTT broker!")

#----------------Motor references----------------------------------
# http://micropython-on-esp8266-workshop.readthedocs.io/en/latest/basics.html
# ESP8266 pins 0, 2, 4, 5, 12, 13, 14 and 15 all support PWM
# Servo Duty Cycle [40-114 OR *30-122* -> 0-180 degree] -> tested 30 to 122
# Duty cycle == Servo Motor Angle
# Using [Pin 12 - Pan (Horizontal)] [Pin 13 - Tilt (Vertical)]

def motorMovement():
    global dCycleX
    global dCycleY
    global HEAT_MAP_SIZE

    # initialise 2D data stores to all 0s
    temperatureData = [[0 for x in range(HEAT_MAP_SIZE)] for y in range(HEAT_MAP_SIZE)]
    rgbData = [[0 for x in range(HEAT_MAP_SIZE)] for y in range(HEAT_MAP_SIZE)]

    # MQTT client initialisation
    client = MQTTClient(machine.unique_id(),"46.101.27.42",port=9001)
    client.connect()

    while True:
        json = ""
        for i in range(0,HEAT_MAP_SIZE):
            servoX.duty(dCycleX)
            dCycleX = (60) if i==(HEAT_MAP_SIZE-1) else (dCycleX+dCycleStep)
            time.sleep(0.5)
            print("i value: " , i, "X Duty Cycle is ",dCycleX,"Y Duty Cycle is ",dCycleY)
            for j in range(0,HEAT_MAP_SIZE):
                servoY.duty(dCycleY)
                dCycleY = (60) if j==(HEAT_MAP_SIZE-1) else (dCycleY+dCycleStep)
                time.sleep(0.5)
                print("j value: " , j, "X Duty Cycle is ",dCycleX,"Y Duty Cycle is ",dCycleY)
                # getRawTemperatureData |> toRGB |> toJSON |> publishToMQTTBroker
                print ("getting temperature data...")
                temperatureData[i][j] = getRawTemperatureData()
                # TMP 007 temperature range = -40 to 125 Celsius
                print ("calculating RGB equivalent of temperature...")
                rgbData[i][j] = list(rawTemperatureDataToRGBHeatMap(20,70,temperatureData[i][j]))
        # after one COMPLETE scan, send data to MQTT broker
        print ("formatting data in JSON format...")
        json = dataToJSON(machine.RTC().datetime(),temperatureData,rgbData)
        print ("final json output!",json)
        time.sleep(1)
        sendDataToMQTTBroker(client,json)
        time.sleep(1)

def start():
    init.initialiseTimeandNetworkConnection()
    time.sleep(1)
    motorMovement()

start()
