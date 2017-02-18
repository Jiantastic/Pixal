import network
import ntptime

# this code is initialised every time ESP8266 gets power, gets real time from NTP server + connect to WiFi
# the do_connect() loop waits until it receives a network connection (GSM/WiFi/Satellite)
# this ensures that the main.py code doesn't execute until a network connection is secured
# modify sta_if.connect('<insert_network_name>','<insert_password>') with your own WiFi network

def initialiseTimeandNetworkConnection():
    # Time formatting issues -> https://github.com/micropython/micropython/issues/2237
    # RTC.datetime(): (year, month, day, weekday, hours, minutes, seconds, subseconds)
    # this issue is handled automatically by ntptime.settime() function
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    def do_connect():
        import network
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect('<insert_network_name>','<insert_password>')
            while not sta_if.isconnected():
                pass
        print('network config:', sta_if.ifconfig())

    do_connect()
    print ("getting time from NTP server...")
    ntptime.settime()