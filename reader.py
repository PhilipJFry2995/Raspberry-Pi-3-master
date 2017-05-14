import time
import json
import requests
import h5py
import numpy
from datetime import datetime, timedelta
from read_sensor import read_data
from email_notification import write_letter

url = 'http://46.101.114.237/static/polls/file.php'
json_path = '/home/pi/project/config10.36.5.157.json'
with open(json_path) as json_file:
  configuration = json.load(json_file)
email = configuration['server']['email']

#Creating file and datasets if not exists
try:
    f = h5py.File("data.hdf5", "r")
except IOError as e:
    print 'Creating new file'
    f = h5py.File("data.hdf5", "w")
    ip_group = f.create_group(configuration['server']['IP'])
    for sensor in configuration['sensors']:
      ip_group.create_dataset(str(sensor['url']), (1,), maxshape=(None,), dtype=[('time', '|S27'),
                                                                            (str(sensor['name']), 'f'),
                                                                            ('active', 'b') ])
else:
  print 'File is ready'
f.close()

notify_max = []
notify_min = []
for i in range(len(configuration['sensors'])):
  notify_max.append(True)
  notify_min.append(True)
counter = 0;
i = 0;

while True:

  counter = counter + 1;
  
  for sensor in configuration['sensors']:
    # Reading data from sensor
    if sensor["active"] == True:
      value = read_data(sensor)
      
      #Getting actual time
      today = datetime.strftime(datetime.now() + timedelta(hours=3), "%Y-%m-%d %H:%M:%S.")
      
      if value != None:
        print('Sensor ' + sensor['metadata']['Sensor ID'] + ' measures ' + str(value))
      if value > sensor['max']:
        if notify_max[i] == True:
          text = 'Warning!\nThe sensor ' + sensor['metadata']['Sensor ID'] + ' value ' + str(value) + ' has exceeded the Max value: ' + str(sensor['max'])
          text = text + ' from ' + configuration['server']['IP'] + '/' + sensor['url'] + ' in ' + today
          write_letter(text, email, sensor['url'])
          notify_max[i] = False
      else:
        notify_max[i] = True
        
      if value < sensor['min']:
        if notify_min[i] == True:
          text = 'Warning!\nThe sensor ' + sensor['metadata']['Sensor ID'] + ' value ' + str(value) + ' is lower than the Min value: ' + str(sensor['min'])
          text = text + ' from ' + configuration['server']['IP'] + '/' + sensor['url'] + ' in ' + today
          write_letter(text, email, sensor['url'])
          notify_min[i] = False
      else:
        notify_min[i] = True
    #Writing to file
    f = h5py.File("data.hdf5", "a")
    dataset = f.get(configuration['server']['IP']).get(sensor['url']) #Getting dataset
    dataset.resize((dataset.len()+1,))
    if sensor["active"] == True:
      dataset[dataset.len()-1] = [(today, value, True)] #Adding new value; True - sensor is active
    else:
      dataset[dataset.len()-1] = [(today, 0, False)] #Adding new value; True - sensor is active
    
    f.close()
    i = i + 1
  
  i = 0;
  #Sending file every 5 minutes (300)
  time.sleep(1);
  if counter == 30:
    counter = 0;
    try:
      files = {'userfile': open('data.hdf5', 'rb')}
      requests.post(url, files=files)
    except requests.ConnectionError:
      # Process data localy
      print 'No Internet connection'
    finally:
      print 'File sent'