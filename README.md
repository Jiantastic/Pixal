# Introducing the Pixal

<insert picture here>

A low cost, real-time, cloud-connected [thermographic camera](https://en.wikipedia.org/wiki/Thermographic_camera).

This project is made by [Wei Jian Wong](https://github.com/Jiantastic), [Ngau Wah Xian](https://github.com/wahxian) and [Jun Wei Sow](https://github.com/junweisow789).




# How it works
<insert graphs+visualisations here>
![alt tag](https://github.com/Jiantastic/embed-trio-IoT/blob/master/images/highlevel.png)


Final JSON output sent to server

```json
{
"time" : "2017-2-14 18:56:30", 
"meanTemperature" : "[[43.35156, 43.375, 44.4375, 45.61719, 46.42188, 47.29688, 47.91406], [46.88282, 44.24219, 42.6875, 41.73438, 41.26563, 41.32813, 42.24219], [42.14063, 39.65625, 38.39063, 37.96875, 37.90625, 38.1875, 38.67188], [38.72656, 36.9375, 35.97656, 35.51563, 35.28125, 35.64063, 35.91406], [35.4375, 34.24219, 33.15625, 32.63281, 32.4375, 32.57813, 33.00781], [33.53125, 32.73438, 32.32031, 31.95313, 31.90625, 31.53906, 31.35937], [31.41406, 31.15625, 31.07813, 31.1875, 31.35937, 31.46875, 31.60156]]", 
"rgb" : "[[[0, 239, 16], [0, 239, 16], [0, 250, 5], [6, 249, 0], [14, 241, 0], [23, 232, 0], [29, 226, 0]], [[19, 236, 0], [0, 248, 7], [0, 232, 23], [0, 222, 33], [0, 217, 38], [0, 218, 37], [0, 227, 28]], [[0, 226, 29], [0, 201, 54], [0, 188, 67], [0, 184, 71], [0, 183, 72], [0, 186, 69], [0, 191, 64]], [[0, 192, 63], [0, 173, 82], [0, 163, 92], [0, 159, 96], [0, 156, 99], [0, 160, 95], [0, 163, 92]], [[0, 158, 97], [0, 146, 109], [0, 135, 120], [0, 129, 126], [0, 127, 128], [0, 129, 126], [0, 133, 122]], [[0, 139, 116], [0, 130, 125], [0, 126, 129], [0, 122, 133], [0, 122, 133], [0, 118, 137], [0, 116, 139]], [[0, 117, 138], [0, 114, 141], [0, 113, 142], [0, 115, 140], [0, 116, 139], [0, 117, 138], [0, 119, 136]]]"
}
```

Breakdown of data sent:

``` time ``` -> On startup, the Pixal queries once from NTP servers and sets its RTC with this information. Subsequent time information do not query from NTP but uses the MicroPython RTC functionality.

``` meanTemperature ``` -> We did several calculations of the temperature measurement delay of the TMP 007. Decided on measuring the average temperature over a 2.5 second interval for each pixel scan

``` rgb ``` -> Using a temperature to [RGB](https://en.wikipedia.org/wiki/RGB_color_model) algorithm as detailed in main.py, we do onboard processing on the ESP8266 by calculating a range of RGB values from raw temperature data gathered from the TMP 007


# Applications


# Problems encountered and how we solved it

image of peace sign

conditions in which sensor works

# Technologies used

**Hardware**

[Adafruit Feather HUZZAH with ESP8266 WiFi](https://www.adafruit.com/product/2821)

[TMP 007 sensor](http://www.ti.com/product/TMP007)

[Two-axis servo motor](https://www.adafruit.com/product/1967)

**Cloud**

[DigitalOcean server](https://www.digitalocean.com/)

[Mosquitto MQTT Broker](https://mosquitto.org/)

[Paho MQTT Python Client](https://eclipse.org/paho/clients/python/)

**Graphs**

[MatPlotLib imshow()](http://matplotlib.org/users/image_tutorial.html) - Plotting RGB data 

# Effective modifications

<3d printed cube, aluminium foil,ultrasonic sensor to measure distance>
The field-of-view of the sensor is limited by enclosing it with a IR shielded enclosure with a small aperture. The measurements of the enclosure is calculated and tabulated in the table below:

![alt tag](https://github.com/Jiantastic/embed-trio-IoT/blob/master/images/Enclosure_Calculation.png)

The customised enclosure is then 3D printed.

![alt tag](https://github.com/Jiantastic/embed-trio-IoT/blob/master/images/3D_printer_Machine.jpg)

# Future Work

Additional sensors will be implemented on the Pixal in the future. This includes a HC-SR04 ultrasonic range sensor.
This will enable more accurate determination of the heat source using triangulation algorithms. Additiional sensor data, such as distance of the object from the sensor can also be collected.

![alt tag](https://github.com/Jiantastic/embed-trio-IoT/blob/master/images/Pixal_perfect.JPG)

Relays and actuators can also be added according to the end applications. 
For example, actuators can be used to turn on fans for warmer areas to improve ventilation.

## Ideas

Provisional ideas:

* PIR motion, IR sensors:  thermal imaging

* smart desk for IR and PIR: HVAC personalised desk ecosystem

0. Various Applications of Thermopiles: http://www.jondetech.com/documents/applications.html

1. Infrared shower body temperature detector - modifies shower temperature based on how cold the human body is

2. Detect number of humans in the area ( do humans emit infrared at a certain wavelength? We can just filter for that particular wavelength) - intruder alarms use passive IR iirc, can use that as a reference

3. Camera/PIR sensor + TMP007(measure object temperature) to achieve something like this -> http://www.flir.co.uk/flirone/ios-android/ (we just need to map temperatures of a certain range to a certain colour to achieve this) . If we have two cameras, we can use triangulation to determine how far the object is from our sensors. All these data can be processed in the "cloud" and visualised onto a webpage. 

  <strong>PROBLEM : is TMP007 capable of getting a range of heat values or just one? if it's just one we wouldn't be able to create a   heat map</strong>
  => operating temp range: -40 to 125 degree celcius and it's within the thermal imaging color scale 
  
  <strong>BUSINESS PROPOSITION : Current infrared camera solutions are expensive, what we have here is a 30ish pound IoT device. Able to deploy these sensors in a forest to record the frequency of movement of animals in a certain locations. As the GPS coordinates of sensors have already been determined via an on-board GPS chip, we can visualise where animals move around in the forest and at what times, useful for scientific research etc etc...</strong>
  
  converting temperature (K) to RGB : https://gist.github.com/paulkaplan/5184275
  
4. Motion detection based on change in temperature

5. Victim Detection robot after Earthquakes like this -> https://www.uni-koblenz.de/~agas/Public/Hahn2011HMF.pdf 

6. At times of epidemics of diseases causing fever, such as SARS coronavirus and Ebola virus disease, non contact IR sensor can be used to check arriving travellers for fever.

7. Able to set a temperature threshold for TMP 007. Sends an ALERT signal if exceed certain threshold (for example). Can be used to detect change/specific objects (human body at 37C?)
8. Smart fever monitoring system: Parents can visualise the body temperature/fever condition of their kids (even when they are away from home etc) through cloud connected smart phone application which records and send alert notification if the value exceeds a certain threshold level.

## Resources

Add useful stuff here.

### ESP8266
*blue LED flickering is fixed

Espressif ESP8266 Resources - https://espressif.com/en/products/hardware/esp8266ex/resources

ESP8266 Wiki - https://github.com/esp8266/esp8266-wiki/wiki

### TMP 007 - https://en.wikipedia.org/wiki/Passive_infrared_sensor

Adafruit TMP 007 C++ Library - https://github.com/adafruit/Adafruit_TMP007_Library

TMP 007 datasheet - http://www.ti.com/lit/ds/symlink/tmp007.pdf

TMP 007 general description - http://www.ti.com/product/TMP007/description

TMP 007 calibration guide (useful FAQ on page 24) - http://www.tij.co.jp/jp/lit/ug/sbou142/sbou142.pdf

Field of View and range of TMP, *heat map shown* - https://youtu.be/GEGiEi6tcVo
-Comment: at 1m - object should be close to sensor if not will be affected by others in the field of view

### PIR sensor

Enocean A5 07 01 PIR detector - https://www.enocean.com/en/enocean_modules_928mhz/ceiling-mounted-occupancy-sensor-eosc-oem-2/user-manual-pdf/ (datasheet)

Available at
https://www.enocean-alliance.org/en/products/peha_easyclick-wall_mounted_occupancy_sensor0/

### I2C

How I2C Communication Works and How To Use It with Arduino - https://youtu.be/6IAkYpmA1DQ

### MicroPython

Official MicroPython docs for ESP8266 - https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/index.html

### MQTT
the BB slides basically sums up what we need to know!

MQTT-micrpython: https://github.com/micropython/micropython-lib/tree/master/umqtt.simple
set up a broker either using PAHO, Mosquitto or mymQTT (mobile)

### ULTrasonic sensor
https://github.com/rsc1975/micropython-hcsr04
