import RPi.GPIO as GPIO

# LED   PIN 14
# LENTA PIN  4
# FAN   PIN 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
# light()
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.LOW)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, GPIO.LOW)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)
