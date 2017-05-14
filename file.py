import h5py

def check_file(configuration):
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