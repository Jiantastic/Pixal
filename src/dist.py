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
