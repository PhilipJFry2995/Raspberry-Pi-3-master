import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import requests
import h5py
import numpy
from datetime import datetime, timedelta

sensor_pin = 23
light_pin = 24
url = 'http://46.101.114.237/static/polls/file.php'
json_path = '/home/debian/project/config10.36.5.157.json'
with open(json_path) as json_file:
  configuration = json.load(json_file)
counter = 0

#Creating file and datasets if not exists
try:
    f = h5py.File("temp_hum.hdf5", "r")
except IOError as e:
    print 'Creating new file'
    f = h5py.File("temp_hum.hdf5", "w")
    ip_group = f.create_group("10.36.5.157")
    #master_group = ip_group.create_group("hydrotermometr")
    temp_dataset = ip_group.create_dataset("hydrotermometr/temperature", (1,), maxshape=(None,), dtype=[('time', '|S27'),
                                                                               ('temperature', 'f'),
                                                                               ('active', 'b') ])
    hum_dataset = ip_group.create_dataset("hydrotermometr/humidity", (1,), maxshape=(None,), dtype=[('time', '|S27'),
                                                                               ('humidity', 'f'),
                                                                               ('active', 'b') ])
    light_dataset = ip_group.create_dataset("illumination", (1,), maxshape=(None,), dtype=[('time', '|S27'),
                                                                               ('illumination', 'f'),
                                                                               ('active', 'b') ])
else:
    print 'File is ready'
f.close()

GPIO.setmode(GPIO.BCM)

while True:
  # Read humidity and temperature
  humidity, sendTemp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, sensor_pin)
  
  # Read illumination
  light = 0
  GPIO.setup(light_pin, GPIO.OUT)
  GPIO.output(light_pin, GPIO.LOW)
  time.sleep(0.1)

  GPIO.setup(light_pin, GPIO.IN)
  while (GPIO.input(light_pin) == GPIO.LOW):
    light += 1
  
  #Getting actual time
  today = datetime.strftime(datetime.now() + timedelta(hours=3), "%Y-%m-%d %H:%M:%S.")

  #Printing results
  print "Humidity = " + str(humidity) + "% Temperature = " + str(sendTemp) + " C Illumination = " + str(light)

  #Writing to file
  f = h5py.File("temp_hum.hdf5", "a")
  
  temp_dataset = f.get("10.36.5.157").get("hydrotermometr/temperature") #Getting dataset
  temp_dataset.resize((temp_dataset.len()+1,))
  temp_dataset[temp_dataset.len()-1] = [(today, sendTemp, True)] #Adding new value; True - sensor is active
  
  hum_dataset = f.get("10.36.5.157").get("hydrotermometr/humidity") #Getting dataset
  hum_dataset.resize((hum_dataset.len()+1,))
  hum_dataset[hum_dataset.len()-1] = [(today, humidity, True)] #Adding new value; True - sensor is active
  
  light_dataset = f.get("10.36.5.157").get("illumination") #Getting dataset
  light_dataset.resize((light_dataset.len()+1,))
  light_dataset[light_dataset.len()-1] = [(today, light, True)] #Adding new value; True - sensor is active
  
  f.close()
  
  #Sendig file to server every hour
  if counter > 4: 
    try:
      files = {'userfile': open('temp_hum.hdf5', 'rb')}
      requests.post(url, files=files)
    except requests.ConnectionError:
      # Process data localy
      print 'No Internet connection'
    finally:
      print 'File sent'
      counter = 0
  #Waiting 5 minutes
  #time.sleep(300) 
  counter = counter + 1