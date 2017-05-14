from gpiozero import LightSensor, Buzzer
import RPi.GPIO as GPIO
import time

LIGHT_SENSOR_1 = 18
LIGHT_SENSOR_2 = 24

light1 = LightSensor(LIGHT_SENSOR_1)
light2 = LightSensor(LIGHT_SENSOR_2)

while(True):
  print light1.value
  print light2.value
  time.sleep(1)


