import h5py
import sys

sys.path.append('/home/pi/project')

import log

logger = log.get_logger()


def inner_json(sensor, ip_group):
    """ recursive search of ending json file """
    if 'submenu' not in sensor:
        url = str(sensor['url'])
        ip_group.create_dataset(url[12:len(url)], (1,), maxshape=(None,), dtype=[('time', '|S27'),
                                                                                 (str(sensor['namesen']), 'f')])
        # ip_group.create_dataset(url[12:len(url)], (1,), maxshape=(None,), dtype=[('time', '|S27'),
        #                                                                              (str(sensor['namesen']), 'f'),
        #                                                                               ('active', 'b') ])
    else:
        for x in sensor['submenu']:
            inner_json(x, ip_group)


def get_file(configuration):
    # Creating file and datasets if not exists
    try:
        f = h5py.File("domain/data.hdf5", "r")
    except IOError:
        logger.info('Creating new file')
        f = h5py.File("data.hdf5", "a")
        ip_group = f.create_group(configuration['IP'])
        for submenu in configuration['menu']:
            inner_json(submenu, ip_group)
    else:
        logger.info('File is ready')
    f.close()
    return h5py.File("domain/data.hdf5", "a")
