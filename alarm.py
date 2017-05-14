import Adafruit_DHT
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)

p = GPIO.PWM(8, 50)
p.start(50)
p2 = GPIO.PWM(36, 300)
p2.start(10)
p3 = GPIO.PWM(40, 20000)
p3.start(100)

input('press any key')

p.stop()
p2.stop()
p3.stop()

