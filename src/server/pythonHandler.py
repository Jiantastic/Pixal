#!/usr/bin/python

# Copyright (c) 2010-2013 Roger Light <roger@atchoo.org>
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Distribution License v1.0
# which accompanies this distribution.
#
# The Eclipse Distribution License is available at
#   http://www.eclipse.org/org/documents/edl-v10.php.
#
# Contributors:
#    Roger Light - initial implementation
# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.

# This shows a simple example of an MQTT subscriber.

import sys
try:
    import paho.mqtt.client as mqtt
except ImportError:
    # This part is only required to run the example from within the examples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import paho.mqtt.client"
    import os
    import inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.client as mqtt

def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    import json
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import numpy as np
    import subprocess

    # process JSON data and save graph in current directory
    a = msg.payload
    aa = a.decode("utf-8")
    aaa = json.loads(aa)
    placeholder = json.loads(aaa['rgb'])
    graphData = np.array(placeholder,dtype=np.uint8)
    plt.imshow(graphData,origin='lower',interpolation='none')
    plt.colorbar()
    plt.suptitle('original heat map',fontsize=20)
    plt.savefig('oriheatmap.png')
    plt.suptitle('interpolated (hanning) heat map',fontsize=20)
    plt.imshow(graphData,origin='lower',interpolation='hanning')
    plt.savefig('interpolatedheatmap.png')
    plt.close()
    # calls a bash script which does further processing and file relocation
    subprocess.call("/home/mosquitto/script.sh")
def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
# connect to MQTT broker located at 46.101.27.42:9001
mqttc.connect("46.101.27.42", 9001, 60)
mqttc.subscribe("embedTrio/#", 0)


mqttc.loop_forever()