# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import json
import os.path

json_path = '/home/pi/project/mqtt_slaves.json'


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("hello/world")
    client.subscribe("onpu/buttonpresses")
    client.subscribe("onpu/temperature")
    client.subscribe("onpu/accelerometer")
    client.subscribe("onpu/accX")
    client.subscribe("onpu/accY")
    client.subscribe("onpu/accZ")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if os.path.isfile(json_path) == False:
        f = open(json_path, 'w')
        f.write('{}')
        f.close()

    with open(json_path) as json_file:
        configuration = json.load(json_file)

    print "Topic: ", msg.topic + '\nMessage: ' + str(msg.payload)
    configuration[msg.topic] = msg.payload

    with open(json_path, 'w') as json_file:
        json.dump(configuration, json_file)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.230", 1884, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
