import json
from auto import auto_mode
from autonomus import autonomus_mode
from semiauto import semiauto_mode
from check_connection import is_connected
import requests

json_path = '/home/pi/project/config10.36.5.157.json'
url = 'http://46.101.114.237/static/polls/file.php'

while True:

  #reloading configuration file
  with open(json_path) as json_file:
    configuration = json.load(json_file)
  
  if configuration['Mode'] != 'autonomus':
    server_connection = is_connected("46.101.114.237", 8000);
    internet_connection = is_connected("www.google.com", 80);
    print 'Server connection: ' + str(server_connection)
    print 'Internet connection: ' + str(internet_connection);
  else:
    server_connection = False
    internet_connection = False
    
  if configuration['Mode'] == 'auto':
    if server_connection:
      print 'auto'
      auto_mode(configuration, url)
    elif internet_connection:
      print 'semi'
      semiauto_mode(configuration, url)
    else:
      print 'autonomus'
      autonomus_mode(configuration)
  elif configuration['Mode'] == 'semiauto':
    if internet_connection:
      print 'semi'
      semiauto_mode(configuration, url)
    else:
      print 'autonomus'
      autonomus_mode(configuration)
  else:
    print 'autonomus'
    autonomus_mode(configuration)