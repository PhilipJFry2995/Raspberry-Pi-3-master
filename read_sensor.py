import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BCM)

def read_data(sensor):
  pin = int(sensor['Pin'])
  if sensor['url'].find('hydrothermometr') > -1:
    value = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
    if sensor['url'].find('temperature') > -1:
      return value[1] #reading temperature
    else: 
      return value[0] #reading humidity
  #reading illumination
  if sensor['url'].find('illumination') > -1:
    resistance = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin, GPIO.IN)
    while (GPIO.input(pin) == GPIO.LOW):
      resistance += 1
    lux = 30000 * math.exp(-0.009 * resistance);
    return round(lux)
  else:
    return 0
  