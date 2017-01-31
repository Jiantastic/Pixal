# embed-trio-IoT
We got this.

## Ideas

1. Infrared shower body temperature detector - modifies shower temperature based on how cold the human body is

2. Detect number of humans in the area ( do humans emit infrared at a certain wavelength? We can just filter for that particular wavelength) - intruder alarms use passive IR iirc, can use that as a reference

3. Camera + TMP007 to achieve something like this -> http://www.flir.co.uk/flirone/ios-android/ (we just need to map temperatures of a certain range to a certain colour to achieve this) . If we have two cameras, we can use triangulation to determine how far the object is from our sensors. All these data can be processed in the "cloud" and visualised onto a webpage. 

  <strong>PROBLEM : is TMP007 capable of getting a range of heat values or just one? if it's just one we wouldn't be able to create a   heat map</strong>
  
  <strong>BUSINESS PROPOSITION : Current infrared camera solutions are expensive, what we have here is a 30ish pound IoT device. Able to deploy these sensors in a forest to record the frequency of movement of animals in a certain locations. As the GPS coordinates of sensors have already been determined via an on-board GPS chip, we can visualise where animals move around in the forest and at what times, useful for scientific research etc etc...</strong>
  
4. Motion detection based on change in temperature

## Resources

Add useful stuff here.

### ESP8266

Espressif ESP8266 Resources - https://espressif.com/en/products/hardware/esp8266ex/resources

ESP8266 Wiki - https://github.com/esp8266/esp8266-wiki/wiki

### TMP 007 - https://en.wikipedia.org/wiki/Passive_infrared_sensor

Adafruit TMP 007 C++ Library - https://github.com/adafruit/Adafruit_TMP007_Library

TMP 007 datasheet - http://www.ti.com/lit/ds/symlink/tmp007.pdf

TMP 007 general description - http://www.ti.com/product/TMP007/description

Field of View and range of TMP, *heat map shown* - https://youtu.be/GEGiEi6tcVo
-Comment: at 1m - object should be close to sensor if not will be affected by others in the field of view

### I2C

How I2C Communication Works and How To Use It with Arduino - https://youtu.be/6IAkYpmA1DQ

### MicroPython

Official MicroPython docs for ESP8266 - https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/index.html

### MQTT


