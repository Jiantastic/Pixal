from machine import I2C
from umqtt.simple import MQTTClient
import time 

# THINK LIKE A FSM
CURRENT_STATE = 0

# (HEAT_MAP_SIZE)^2 = how big the heat map is
HEAT_MAP_SIZE = 16

# initialise 2D heat map to all 0s
temperatureData = [[0 for x in range(HEAT_MAP_SIZE)] for y in range(HEAT_MAP_SIZE)]


# TODO
# 1. Get real time, cause we want to timestamp our JSON data with time
# 2. Store temperature data 

def storeRawTemperatureData():

    # 1 = local temperatureData
    # 3 = object temperatureData
    from machine import Pin,I2C
    import ubinascii
    i2c = I2C(scl=Pin(5),sda=Pin(4),freq=100000)

    data = i2c.readfrom_mem(64,3,2)
    finalData = ubinascii.hexlify(bytearray(data))
    stringHex = finalData.decode('ascii')
    hex_int = int(stringHex, 16)
    finalTemperatureData = (hex_int >> 2) * 0.03125
    finalTemperatureData

# can just test this with dummy values, matplotlib imshow, colorbar() to plot RGB values for testing
def rawTemperatureDataToRGBHeatMap():


def dataToJSON():


def sendDataToMQTTBroker():
# connect to EEERover network
import network
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('EEERover','exhibition')
sta_if.isconnected()

# Connect to MQTT
from umqtt.simple import MQTTClient

client = MQTTClient(machine.unique_id(),"192.168.0.10")
client.connect()
client.publish("this works holy shit",bytes("Embed Trio damn pro","utf-8"))

#----------------Motor references----------------------------------
# http://micropython-on-esp8266-workshop.readthedocs.io/en/latest/basics.html - Tutorial on setting up 
# ESP8266 pins 0, 2, 4, 5, 12, 13, 14 and 15 all support PWM
# Servo Duty Cycle [40-114 OR *30-122* -> 0-180 degree]
# Duty cycle == Servo Motor Angle
# Using [Pin 12 - Pan (Horizontal)] [Pin 13 - Tilt (Vertical)]

# Import PWM and Pin Libraries
from machine import Pin, PWM
dCycleP = 30
dCycleT = 30
dCycleStep = TBD 
max = 4          #Maximum iteration times 

#Initialise angle as 0 -> duty(30) and Pin allocation
servoP = PWM(Pin(12), freq=50, duty=dCycleP)
servoT = PWM(Pin(13), freq=50, duty=dCycleT)

#2 for loops to loop over every pixel
def motorMovement():
    # get CURRENT_STATE, move according to matrix size
    for i in max:
        servoP.duty(dCycleP)
        global dCycleP = (dCycleT+dCycleStep) if counter<max else (dCycleP)
        #insert code to read and send temp data and send to broker
        for j in max:
            servoT.duty(dCycleT)
            global dCycleT = (dCycleT+dCycleStep) if counter<max else (dCycleT)
            #insert code to read and send temp data and send to broker
            
#-----------------------------------------------------------------------------------------
    
def updateState():
    if CURRENT_STATE == (HEAT_MAP_SIZE * HEAT_MAP_SIZE):

def debugOutput():


# consider declaring def main here, but test each individual function here first!

