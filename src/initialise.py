from machine import Pin,I2C,PWM
from umqtt.simple import MQTTClient
import time 
import network
import machine
import ubinascii
import ujson
import ntptime


# two functions here, initialiseNetworkConnection() AND getRealTime()
# get to same wifi network, then get real time from MQTTBroker
# this code should be initialised on startup
# ampy -p /dev/tty.SLAB_USBtoUART put ampy.py
# NOTES: there is a time delay between sucessful wifi connection
# how this works: 
# import initialise as init
# init.initialiseTimeandNetworkConnection()

def initialiseTimeandNetworkConnection():
    # Time formatting issues -> https://github.com/micropython/micropython/issues/2237
    # RTC.datetime(): (year, month, day, weekday, hours, minutes, seconds, subseconds)
    print ("getting time from NTP server...")
    time.sleep(0.5)
    ntptime.settime()

    # connect to network
    print ("connecting to network...")
    time.sleep(0.5)
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)
    
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    #sta_if.connect('EEERover','exhibition')
    sta_if.connect('VM2708191','tqGtthwD4gpm')
    time.sleep(0.5)     # make sure connection is correctly established
    print("connection to Wifi: ", sta_if.isconnected())


# esys/time <- subscribe to this, wait for real time, just do this once at start, then esp8266 will keep track of time on it's own



# REAL_TIME = 0
# realTime = True

# def sub_cb(topic, msg):
#     print((topic, msg))
#     getRealTime = False

# b'{"date":"2017-01-12 23:16:43+00:00"}')

# def getRealTime():
#     client = MQTTClient(machine.unique_id   (),"192.168.0.10")
#     client.set_callback(sub_cb)
#     client.connect()
#     client.subscribe("esys/time")
#     while realTime:
#         client.check_msg()
#         time.sleep(1)
#         # find a way to kill the application after I get a valid timestamp


#     client.disconnect()




# a = b'{"date":"2017-01-12 22:16:43+00:00"}'
# b = ujson.dumps(a)
# c = ujson.loads(b)
# d = ujson.loads(c)
# d['date']

# year = int(d['date'][0:4])
# month = int(d['date'][5:7])
# day = int(d['date'][8:10])
# hour = int(d['date'][11:13])
# minute = int(d['date'][14:16])
# second = int(d['date'][17:19])

# rtc = machine.RTC()
# rtc.datetime((year,month,day,hour,minute,second,0,0))
# print ("initialised time to ",rtc.datetime())


    # use machine.RTC library
    # rtc = machine.RTC()
    # rtc.datetime((2014, 5, 1, 0, 4, 13, 0, 0)) <- documentation is wrong
    # rtc.datetime() <- get real time, documentation is wrong
    # settings to use rtc.datetime((year,month,day,hour,minute,second,0,0))

# get this data -> b'{"date":"2017-01-12 23:16:43+00:00"}' -> ujson dump -> get year time date 



# b'{"date":"2017-01-12 23:43:44+00:00"}'
# b'{"date":"2017-01-12 23:44:44+00:00"}