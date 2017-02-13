# main.py and initialise.py is fully functional :D - do not directly modify this file without testing!
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
dCycleStep = 6
HEAT_MAP_SIZE = 4          # Maximum iteration times , (HEAT_MAP_SIZE)^2 = how big the heat map is
TEMP_SAMPLE_SIZE=4         # Sample size of the temperature data to obtain a more accurate mean

#Initialise angle as 0 -> duty(30) and Pin allocation
servoX = PWM(Pin(15), freq=50, duty=dCycleX)
servoY = PWM(Pin(13), freq=50, duty=dCycleY)

# TODO:
# 1. Exception handling?
# 2. Global import of Python modules?
# 3. Integrate Ultrasound Sensor info?




def getRawTemperatureData():
    sum_tmp=0
    # 1 = local temperatureData
    # 3 = object temperatureData
    i2c = I2C(scl=Pin(5),sda=Pin(4),freq=100000)
    for k in range(0,TEMP_SAMPLE_SIZE):
         temperature_reading = i2c.readfrom_mem(64,3,2)
         byteHex = ubinascii.hexlify(bytearray(temperature_reading))
         stringHex = byteHex.decode('ascii')
         hex_int = int(stringHex, 16)
         #finalTemperatureData [k] = (hex_int >> 2) * 0.03125
         sum_tmp= sum_tmp + (hex_int >> 2) * 0.03125
         time.sleep(0.3)
    mean_temp= sum_tmp / TEMP_SAMPLE_SIZE
    time.sleep(0.5)
    print ("the mean data is ", mean_temp)
    return mean_temp

# can just test this with dummy values, matplotlib imshow, colorbar() to plot RGB values for testing
# http://stackoverflow.com/questions/20792445/calculate-rgb-value-for-a-range-of-values-to-create-heat-map
def rawTemperatureDataToRGBHeatMap(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    time.sleep(0.5)
    return r, g, b

# insert array of data, iterate through entire JSON file and print that shit
# replace this with RGB arrays
# final data output: {time: 2017-15-1, temperature : [25.6,30.3,35.7],rgb : [[1,2,3],[4,5,6],[7,8,9]]}
# MARK SCHEME : Conversion to real units and use of triggering or statistics. Messages formatted in JSON

# RTC.datetime(): (year, month, day, weekday, hours, minutes, seconds, subseconds)
# year-month-day-hour-minutes-seconds
def dataToJSON(currentTime,temperatureData,rgbData):

    formatTime = str(currentTime[0]) + '-' + str(currentTime[1]) + '-' + str(currentTime[2]) + ' ' + str(currentTime[4]) + ':' + str(currentTime[5]) + ':' + str(currentTime[6])
    time = '{"time" : ' + '"' + formatTime + '"' + ', '
    temperature = '"temperature" : ' + '"' + str(temperatureData) + '"' + ', '
    rgb = '"rgb" : ' + '"' + str(rgbData) + '"' + '}'
    jsonString = time + temperature + rgb

    return jsonString

def sendDataToMQTTBroker(client,jsonData):
# IMPORTANT: connect to EEERover network

    # home network broker : 192.168.0.15, EERover broker 192.168.0.10
    client.publish("esys/EmbedTrio",bytes(jsonData,"utf-8"))
    print("sent data to MQTT broker!")

# consider declaring def main here, but test each individual function here first!


#----------------Motor references----------------------------------
# http://micropython-on-esp8266-workshop.readthedocs.io/en/latest/basics.html - Tutorial on setting up
# ESP8266 pins 0, 2, 4, 5, 12, 13, 14 and 15 all support PWM
# Servo Duty Cycle [40-114 OR *30-122* -> 0-180 degree] -> tested 30 to 122
# Duty cycle == Servo Motor Angle
# Using [Pin 12 - Pan (Horizontal)] [Pin 13 - Tilt (Vertical)]

# Import PWM and Pin Libraries# Import PWM and Pin Libraries
# Import PWM and Pin Libraries

def motorMovement():
    global dCycleX
    global dCycleY
    global HEAT_MAP_SIZE

    # initialise 2D data stores to all 0s
    temperatureData = [[0 for x in range(HEAT_MAP_SIZE)] for y in range(HEAT_MAP_SIZE)]
    rgbData = [[0 for x in range(HEAT_MAP_SIZE)] for y in range(HEAT_MAP_SIZE)]

    # MQTT client initialisation
    client = MQTTClient(machine.unique_id(),"192.168.0.10")
    client.connect()

    while True:
        json = ""
        for i in range(0,HEAT_MAP_SIZE):
            servoX.duty(dCycleX)
            dCycleX = (60) if i==(HEAT_MAP_SIZE-1) else (dCycleX+dCycleStep)
            time.sleep(0.5)
            print("I value: " , i, "X Duty Cycle is ",dCycleX,"Y Duty Cycle is ",dCycleY)
            for j in range(0,HEAT_MAP_SIZE):
                servoY.duty(dCycleY)
                dCycleY = (60) if j==(HEAT_MAP_SIZE-1) else (dCycleY+dCycleStep) # if j<max else (dCycleY)
                time.sleep(0.5)
                print("J value: " , i, "X Duty Cycle is ",dCycleX,"Y Duty Cycle is ",dCycleY)
                #insert code to read and send temp data and send to broker
                # getRawTemperatureData |> toRGB |> toJSON |> publishToMQTTBroker
                print ("getting temperature data...")
                temperatureData[i][j] = getRawTemperatureData()
                # TMP 007 temperature range = -40 to 125 Celsius
                print ("calculating RGB equivalent of temperature...")
                rgbData[i][j] = list(rawTemperatureDataToRGBHeatMap(-40,125,temperatureData[i][j]))
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
