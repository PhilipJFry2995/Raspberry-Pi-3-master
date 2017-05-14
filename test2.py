import RPi.GPIO as GPIO, time, os, math

pin = 24

GPIO.setmode(GPIO.BCM)
#comment
while True:
  reading = 0
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.LOW)
  time.sleep(0.1)

  GPIO.setup(pin, GPIO.IN)
  while (GPIO.input(pin) == GPIO.LOW):
    reading += 1
  print 'Resistance ' + str(reading) + ' R'
  lux = 30000 * math.exp(-0.009 * reading);
  print 'LUX %7.2f' % lux;