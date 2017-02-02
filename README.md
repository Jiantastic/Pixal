# embed-trio-IoT
We got this.

## Ideas

Provisional ideas:

* PIR motion, IR sensors:  thermal imaging

*smart desk for IR and PIR: HVAC personalised desk ecosystem

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

### I2C

How I2C Communication Works and How To Use It with Arduino - https://youtu.be/6IAkYpmA1DQ

### MicroPython

Official MicroPython docs for ESP8266 - https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/index.html

### MQTT
the BB slides basically sums up what we need to know!

MQTT-micrpython: https://github.com/micropython/micropython-lib/tree/master/umqtt.simple
set up a broker either using PAHO, Mosquitto or mymQTT (mobile)

