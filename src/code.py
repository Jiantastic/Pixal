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
# Servo Duty Cycle [40-114 OR *30-122* -> 0-180 degree] -> tested 30 to 122
# Duty cycle == Servo Motor Angle
# Using [Pin 12 - Pan (Horizontal)] [Pin 13 - Tilt (Vertical)]

# Import PWM and Pin Libraries# Import PWM and Pin Libraries
# Import PWM and Pin Libraries
from machine import Pin, PWM
import time

dCycleX = 60
dCycleY = 60
dCycleStep = 6 
max = 4          #Maximum iteration times 

#Initialise angle as 0 -> duty(30) and Pin allocation
servoX = PWM(Pin(15), freq=50, duty=dCycleX)
servoY = PWM(Pin(13), freq=50, duty=dCycleY)

#2 for loops to loop over every pixel
def motorMovement():
    # get CURRENT_STATE, move according to matrix size
    global dCycleX
    global dCycleY
    
    while True:
        for i in range(0,max):
            servoX.duty(dCycleX)
            dCycleX = (60) if i==3 else dCycleX+dCycleStep
            time.sleep(0.5)
            print("I value: " , i, "X Duty Cycle is ",dCycleX,"Y Duty Cycle is ",dCycleY)
            #insert code to read and send temp data and send to broker
            for j in range(0,max):
                servoY.duty(dCycleY)
                dCycleY = (dCycleY+dCycleStep) # if j<max else (dCycleY)
                time.sleep(0.5)
                print("J value: " , i, "X Duty Cycle is ",dCycleX,"Y Duty Cycle is ",dCycleY)
                #insert code to read and send temp data and send to broker
            dCycleY=60   

motorMovement()
#-----------------------------------------------------------------------------------------

#----------------------------HC-SR04 Ultrasonic Rangefinder--------------------------------
import machine, time
from machine import Pin

# ESP8266 pins 0, 2, 4, 5, 12, 13, 14 and 15 are all GPIO
#initialise pins for trigger output and echo input
trigger_pin = 0
echo_pin = 2

#initialise pins
echo_timeout_us = 20 #Max time to return echo in us
trigger = Pin(trigger_pin, mode = Pin.OUT, pull=none)
echo = Pin(echo_pin, mode=Pin.IN, pull=None)

trigger.low() #documentation does not have low. Try value() instead

def send_pulse_measure_dist():
	
	# Send Trigger out 
	trigger.low() # Stabilize the sensor
    time.sleep_us(5)
    trigger.high()
    # Send a 10us pulse.
    time.sleep_us(10)
    trigger.low()
    try:
        pulse_time = machine.time_pulse_us(echo_pin, 1, echo_timeout_us)
        mm = pulse_time * 100 // 582
        print mm 
    except OSError as ex:
        if ex.args[0] == 110: # 110 = ETIMEDOUT
            raise OSError('Out of range')
        raise ex
    #Receive pulse echo back and calculate distance

    # To calculate the distance we get the pulse_time and divide it by 2 
    # (the pulse walk the distance twice) and by 29.1 becasue
    # the sound speed on air (343.2 m/s), that It's equivalent to
    # 0.34320 mm/us that is 1mm each 2.91us
    # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 

send_pulse_measure_dist()

#-------------------------------------------------------------------------------------


    
def updateState():
    if CURRENT_STATE == (HEAT_MAP_SIZE * HEAT_MAP_SIZE):

def debugOutput():


# consider declaring def main here, but test each individual function here first!

