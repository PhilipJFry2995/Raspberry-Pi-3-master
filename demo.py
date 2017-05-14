from gpiozero import LightSensor, Buzzer
import Adafruit_DHT
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

MAX_TEMPERATURE = 15
MIN_LIGHT = 0.7

LIGHT_SENSOR_1 = 18  # 12
LIGHT_SENSOR_2 = 24  # 18

HYRDO_1 = 25
HYRDO_2 = 23

LED = 14  # 8
FAN = 21  # 40
SOUND = 16  # 36

LED_TAPE = 4  # 7

GPIO.setup(LED_TAPE, GPIO.OUT)
tape_pwm = GPIO.PWM(LED_TAPE, 100)
tape_pwm.start(0)

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(SOUND, GPIO.OUT)
GPIO.setup(FAN, GPIO.OUT)

p = GPIO.PWM(LED, 50)
p.start(0)
p2 = GPIO.PWM(SOUND, 1500)
p2.start(0)
p3 = GPIO.PWM(FAN, 20000)
p3.start(0)

light1 = LightSensor(LIGHT_SENSOR_1)
light2 = LightSensor(LIGHT_SENSOR_2)

LIGHT_ON = False

while True:
    hydroterm1 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, HYRDO_1)
    print 'temperature1:' + str(hydroterm1[1])  # temperature
    print 'humidity1:   ' + str(hydroterm1[0])  # hydro

    hydroterm2 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, HYRDO_2)
    print 'temperature2:' + str(hydroterm2[1])  # temperature
    print 'humidity2:   ' + str(hydroterm2[0])  # hydro

    print 'light1:      ' + str(light1.value)
    print 'light2:      ' + str(light2.value)

    light = (light1.value + light2.value) / 2
    print 'av. light:   ' + str(light)

    print '**************'

    if light < MIN_LIGHT:
        if LIGHT_ON == False:
            for dc in range(0, 101, 1):
                tape_pwm.ChangeDutyCycle(dc)
                time.sleep(0.02)
            LIGHT_ON = True
    else:
        if LIGHT_ON:
            for dc in range(100, -1, -1):
                tape_pwm.ChangeDutyCycle(dc)
                time.sleep(0.02)
        # tape_pwm.ChangeDutyCycle(0)
        LIGHT_ON = False

    if hydroterm1[1] > MAX_TEMPERATURE or hydroterm2[1] > MAX_TEMPERATURE:
        p.ChangeDutyCycle(100)
        p2.ChangeDutyCycle(10)
        time.sleep(0.3)
        p.ChangeDutyCycle(0)
        p2.ChangeDutyCycle(0)

        p3.ChangeDutyCycle(100)
    else:
        p.ChangeDutyCycle(0)
        p2.ChangeDutyCycle(0)
        p3.ChangeDutyCycle(0)
