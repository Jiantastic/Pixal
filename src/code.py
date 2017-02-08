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


def motorMovement():
    # get CURRENT_STATE, move according to matrix size
    
def updateState():
    if CURRENT_STATE == (HEAT_MAP_SIZE * HEAT_MAP_SIZE):

def debugOutput():


# consider declaring def main here, but test each individual function here first!

