from file_check import get_file
from read_sensor import read_data
from datetime import datetime, timedelta
import time
import h5py

def inner_json(sensor, f, configuration):
    """ recursive search of ending json file """
    if 'submenu' not in sensor:
      if sensor['Active'] == 'true':
        value = read_data(sensor)
        
        # TODO processing data localy
        
        print sensor['url'] + ' ' + str(value)
        #Getting actual time
        today = datetime.strftime(datetime.now() + timedelta(hours=3), "%Y-%m-%d %H:%M:%S.")
        #Writing data to file
        dataset = f.get(sensor['url']) #Getting dataset
        dataset.resize((dataset.len()+1,))
        dataset[dataset.len() - 1] = [(today, value, True)] #Adding new value; True - sensor is active
        
    else:
        for x in sensor['submenu']:
            inner_json(x, f, configuration)

def autonomus_mode(configuration):
  
  #while True: 
    
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
      return
        
  #Creating new file if not exist
  get_file(configuration)
  f = h5py.File("data.hdf5", "a")
  
  #Reading data from sensors
  for submenu in configuration['menu']:
    inner_json(submenu, f, configuration)
    
  f.close()