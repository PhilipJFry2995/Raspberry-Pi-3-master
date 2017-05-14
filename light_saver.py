from gpiozero import LightSensor, Buzzer
from datetime import datetime
import time
import RPi.GPIO as GPIO
import math

LIGHT_SENSOR_1 = 18  # 12
LIGHT_SENSOR_2 = 24  # 18

light1 = LightSensor(LIGHT_SENSOR_1)
light2 = LightSensor(LIGHT_SENSOR_2)


def read_data(pin):
    resistance = 0
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(pin, GPIO.IN)
    while GPIO.input(pin) == GPIO.LOW:
        resistance += 1
    return str(30000 * math.exp(-0.009 * resistance))  # Lux


while True:
    value1 = str(light1.value)
    print('light1:      ' + value1)
    value2 = str(light2.value)
    print('light2:      ' + value2)
    print('******')

    now = datetime.now()
    seconds_since_midnight = str(int(round((now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())))

    f = open('light_data.csv', 'a')
    f.write(seconds_since_midnight + ';' + value1 + ';' + value2 + '\n')
    f.close()

    value1 = read_data(LIGHT_SENSOR_1)
    print('light1:      ' + value1)
    value2 = read_data(LIGHT_SENSOR_2)
    print('light2:      ' + value2)

    f = open('light_data2.csv', 'a')
    f.write(seconds_since_midnight + ';' + value1 + ';' + value2 + '\n')
    f.close()

    time.sleep(90)
