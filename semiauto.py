import domain.file_check as file_manager
import hardware.read_sensor as sensor_reader
import network.notification as notification_sender
import network.email_notification as email_sender
import network.check_connection as connection
import time
import h5py
import requests
import log
from datetime import datetime, timedelta

sensor_num = 0
notify_max = []
notify_min = []
i = 0

logger = log.get_logger()


def inner_json(sensor, f, configuration):
    """ recursive search of ending json file """
    global notify_max
    global notify_min
    global i

    if 'submenu' not in sensor:
        if sensor['Active'] == 'true':
            value = sensor_reader.read_data(sensor)

            # TODO processing data locally

            logger.info(sensor['url'] + ' ' + str(value))
            # Getting actual time
            today = datetime.strftime(datetime.now() + timedelta(hours=3), "%Y-%m-%d %H:%M:%S.")
            # Writing data to file
            dataset = f.get(sensor['url'])  # Getting dataset
            dataset.resize((dataset.len() + 1,))
            # dataset[dataset.len() - 1] = [(today, value, True)] #Adding new value; True - sensor is active
            dataset[dataset.len() - 1] = [(today, value)]  # Adding new value; True - sensor is active

            # Checking critical parameters and sending notification
            if sensor['Critical'] == 'true':
                if value > int(sensor['MaxNorma']):
                    if notify_max[i]:
                        text = 'Warning!\nThe sensor ' + sensor['url'] + ' value ' + str(
                            value) + ' has exceeded the Max value: ' + str(sensor['MaxNorma'])
                        text = text + ' from ' + configuration['IP'] + '/' + sensor['url'] + ' in ' + today
                        email_sender.write_letter(text, configuration['Email'], sensor['url'])
                        notify_max[i] = False
                else:
                    # turn_off()
                    notify_max[i] = True

                if value < int(sensor['MinNorma']):
                    if notify_min[i]:
                        text = 'Warning!\nThe sensor ' + sensor['url'] + ' value ' + str(
                            value) + ' is lower than the Min value: ' + str(sensor['MinNorma'])
                        text = text + ' from ' + configuration['IP'] + '/' + sensor['url'] + ' in ' + today
                        email_sender.write_letter(text, configuration['Email'], sensor['url'])
                        notify_min[i] = False
                else:
                    notify_min[i] = True
            i = i + 1
    else:
        for x in sensor['submenu']:
            inner_json(x, f, configuration)


def get_sensors_number(sensor):
    global sensor_num
    """ recursive search of ending json file """
    if 'submenu' not in sensor:
        sensor_num = sensor_num + 1
    else:
        for x in sensor['submenu']:
            get_sensors_number(x)


def semiauto_mode(configuration, url):
    counter = 0
    for submenu in configuration['menu']:
        get_sensors_number(submenu)  # counting number of sensors

    global notify_max
    notify_max = []
    global notify_min
    notify_min = []

    global sensor_num
    for j in range(sensor_num):
        notify_max.append(True)
        notify_min.append(True)
    sensor_num = 0

    while True:
        # checking connection to server
        if configuration['Mode'] == 'semiauto':
            pass
        else:
            server_connection = connection.is_connected("46.101.114.237", 8000)
            if server_connection:
                return

        # checking mode changing
        try:
            f = open('mode', 'r')
            mode_changed = f.readline()
            f.close()
        except IOError:
            mode_changed = '0'
            logger.error('IOError: Trouble reading mode file')

        # Working mode has been changed, return to main program
        if mode_changed != '0':
            logger.warning('Mode changed')
            try:
                f = open('mode', 'w')
                f.write('0')
                f.close()
            except IOError:
                logger.error('IOError: Trouble writing to mode file')
            finally:
                return

        # Creating new file if not exist
        f = file_manager.get_file(configuration)
        # f = h5py.File("data.hdf5", "a")

        # Reading data from sensors
        for submenu in configuration['menu']:
            inner_json(submenu, f, configuration)

        f.close()

        # setting i to zero
        global i
        i = 0

        # Sending file every 5 minutes (300)
        time.sleep(1)
        if counter == 5:
            counter = 0
            try:
                files = {'userfile': open('data.hdf5', 'rb')}
                requests.post(url, files=files)
                notification_sender.send_notification('updateHDF', '46.101.114.237', 9091, 0)
            except requests.ConnectionError:
                logger.error('Cannot connect to server')
                logger.error('File not sent')
                break
