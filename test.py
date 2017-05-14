import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

SOUND = 16#36

GPIO.setup(SOUND, GPIO.OUT)

p2 = GPIO.PWM(SOUND, 5000)
p2.start(0)

while True:
  for dc in range(0, 101, 1):
    p2.ChangeDutyCycle(dc)
    time.sleep(0.2)
  for dc in range(100, -1, -1):
    p2.ChangeDutyCycle(dc)
    time.sleep(0.2)