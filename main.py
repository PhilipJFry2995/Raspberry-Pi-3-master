import json
import network.check_connection as connection
import log
from auto import auto_mode
from autonomus import autonomus_mode
from semiauto import semiauto_mode

# json_path = '/home/pi/project/config10.36.5.157.json'
json_path = '/home/pi/project/config_backup.json'
url = 'http://46.101.114.237/static/polls/file.php'

logger = log.get_logger()
logger.info('Application started')

while True:

    # reloading configuration file
    with open(json_path) as json_file:
        configuration = json.load(json_file)

    if configuration['Mode'] != 'autonomus':
        server_connection = connection.is_connected("46.101.114.237", 8000)
        internet_connection = connection.is_connected("www.google.com", 80)
        logger.info('Server connection: ' + str(server_connection))
        logger.info('Internet connection: ' + str(internet_connection))
    else:
        server_connection = False
        internet_connection = False

    if configuration['Mode'] == 'auto':
        if server_connection:
            logger.info('mode:auto')
            auto_mode(configuration, url)
        elif internet_connection:
            logger.info('mode:semi')
            semiauto_mode(configuration, url)
        else:
            logger.info('mode:autonomus')
            autonomus_mode(configuration)
    elif configuration['Mode'] == 'semiauto':
        if internet_connection:
            logger.info('mode:semi')
            semiauto_mode(configuration, url)
        else:
            logger.info('mode:autonomus')
            autonomus_mode(configuration)
    else:
        logger.info('mode:autonomus')
        autonomus_mode(configuration)

logger.info('Application finished')
