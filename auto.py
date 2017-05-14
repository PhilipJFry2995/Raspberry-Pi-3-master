from file_check import get_file
from read_sensor import read_data
from notification import send_notification
from datetime import datetime, timedelta
import time
import h5py
import requests

def inner_json(sensor, f, configuration):
    """ recursive search of ending json file """
    if 'submenu' not in sensor:
      if sensor['Active'] == 'true':
        value = read_data(sensor)
        print sensor['url'] + ' ' + str(value)
        #Getting actual time
        today = datetime.strftime(datetime.now() + timedelta(hours=3), "%Y-%m-%d %H:%M:%S.")
        #Writing data to file
        dataset = f.get(sensor['url']) #Getting dataset
        dataset.resize((dataset.len()+1,))
        #dataset[dataset.len() - 1] = [(today, value, True)] #Adding new value; True - sensor is active
        dataset[dataset.len() - 1] = [(today, value)] #Adding new value;
        
    else:
        for x in sensor['submenu']:
            inner_json(x, f, configuration)

def auto_mode(configuration, url):

  counter = 0
  while True:
    #checking mode changing 
    try:
      f = open('mode', 'r')
      mode_changed = f.readline()
      f.close()
    except IOError:
      print 'IOError: Trouble reading mode file'

    #Working mode has been changed, return to main programm
    if (mode_changed != '0'):
      print 'Mode changed'
      try:
        f = open('mode', 'w')
        f.write('0')
        f.close()
      except IOError:
        print 'IOError: Trouble writing to mode file'
      finally:
        break
    
    #Main programm
    counter = counter + 1;
    
    #Creating new file if not exist
    get_file(configuration)
    f = h5py.File("data.hdf5", "a")
    
    #Reading data from sensors
    for submenu in configuration['menu']:
      inner_json(submenu, f, configuration)
    
    f.close()
    #Sending file every 5 minutes (300)
    time.sleep(60);
    if counter == 5:
      counter = 0;
      try:
        files = {'userfile': open('data.hdf5', 'rb')}
        requests.post(url, files=files)
        #send_notification('updateHDF', '46.101.114.237', 9091, 0)
        print 'File sent'
      except requests.ConnectionError:
        print 'Cannot connect to server'
        print 'File not sent'
        #changing mode to semiauto
        break