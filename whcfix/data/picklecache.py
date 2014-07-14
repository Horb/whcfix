import os
import pickle
import time


class PickleCache(object):

    def __init__(self, ref, seconds_duration):
        self.ref = ref
        self.seconds_duration = seconds_duration

    def dump(self, obj):
        with open(self._path_to_cache_file, 'w') as pickleFile:
            pickle.dump(obj, pickleFile)

    def load(self):
        with open(self._path_to_cache_file) as pickleFile:
            return pickle.load(pickleFile)

    def exists(self):
        if os.path.exists(self._path_to_cache_file):
            ageOfCacheInSeconds = time.time() - os.path.getctime(self._path_to_cache_file)
            if  ageOfCacheInSeconds > self.seconds_duration:
                # The cache is out of date
                return False
            return True
        else:
            return False

    @property
    def _path_to_cache_file(self):
        return os.path.join(os.getcwd(), self.ref + '.pickle')

