# Introducing the Pixal

<insert picture here>

A low cost, real-time, cloud-connected [thermographic camera](https://en.wikipedia.org/wiki/Thermographic_camera).

This project is made by [Wei Jian Wong](https://github.com/Jiantastic), [Ngau Wah Xian](https://github.com/wahxian) and [Jun Wei Sow](https://github.com/junweisow789).




# How it works
![alt tag](https://github.com/Jiantastic/embed-trio-IoT/blob/master/images/highlevel.png)

## Step 1 - Gathering raw temperature data

We have the TMP 007 sensor attached to a 2-axis servo. We have the 2-axis servo move in a square matrix (similar to the picture shown below) in X and Y directions. We then use the TMP 007 to measure 1 pixel worth of temperature data for approximately 2.5 seconds to get an accurate(averaged) temperature reading. We repeat this for however large the square matrix is ( adjustable with the HEAT_MAP_SIZE constant ), or in the example image below a 4x4 matrix. 

![alt tag](https://github.com/Jiantastic/embed-trio-IoT/blob/master/images/matrix.jpg)

## Step 2 - Onboard processing

The temperature data collected is then turned into RGB values according to an algorithm. This RGB data is then sent to the server, alongside the current time and mean temperature data in JSON format. The ESP8266 will connect to your desired wireless network (GSM/WiFi/Satellite) and send this data to your designated server.

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


## Step 3 - Cloud processing

We have set up an Mosquitto MQTT broker which is listening continuously for new data. Once it has received new data, it will do additional processing, graph generation and file relocation to generate an image to display on a web page.

This is done with the Paho MQTT Python library and Bash scripts.

Here is an example output under contrived conditions ( you can get a more accurate result with a better sensor/further modications )

![alt tag](https://github.com/Jiantastic/embed-trio-IoT/blob/master/images/exampleHeatMap.png)

This image shows the relative hot and cold areas within an image where red is hotter. To produce this image, we had someone do a [V sign](https://en.wikipedia.org/wiki/V_sign) in front of the sensor. The red coloured areas in the graph correspond to a human hand.

# Applications


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

# Modifications

The field-of-view of the sensor is limited by enclosing it with a IR shielded enclosure (like aluminium foil) with a small aperture. The measurements of the enclosure is calculated and tabulated in the table below:

![alt tag](https://github.com/Jiantastic/embed-trio-IoT/blob/master/images/Enclosure_Calculation.png)

The customised enclosure is then 3D printed.

![alt tag](https://github.com/Jiantastic/embed-trio-IoT/blob/master/images/3D_printer_Machine.jpg)


# Problems and limitations encountered

Our limitation here was the TMP 007 sensor. As the TMP 007 only measures a single temperature value, we have to put it on a 2-axis servo to generate a heat map. It takes about 40 seconds to produce a 4x4 heat map. However, if you had a larger array of non-contact IR sensors - say a 64x64 IR sensors with a smaller field-of-view (FOV) per sensor, you would be able to generate a far larger, more accurate heat map with a fraction of the time.

We attempted to use a 3D printed IR enclousure wrapped in aluminium foil to limit the TMP 007 FOV according to the specifications stated by Texas Instruments but on hindsight it would have produced better results if we had an enclosure directly on top of the sensor as explained in this [video](https://youtu.be/GEGiEi6tcVo).

# Future Work

Additional sensors will be implemented on the Pixal in the future. This includes a HC-SR04 ultrasonic range sensor.
This will enable more accurate determination of the heat source using triangulation algorithms. Additiional sensor data, such as distance of the object from the sensor can also be collected.

![alt tag](https://github.com/Jiantastic/embed-trio-IoT/blob/master/images/Pixal_perfect.JPG)

Relays and actuators can also be added according to the end applications. 
For example, actuators can be used to turn on fans for warmer areas to improve ventilation.
