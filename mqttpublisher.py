# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt

mqttc = mqtt.Client("python_pub")
mqttc.connect("192.168.1.230", 1884)
mqttc.publish("hello/world", "Happy new world")
mqttc.loop(2) #timeout = 2s