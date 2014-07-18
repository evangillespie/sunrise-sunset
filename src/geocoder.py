from astral import Location, GoogleGeocoder
from .enums import FILE_GEOCODER_PATH
from .exceptions import LocationNotFoundError
import json
import pickle

class FileGeocoder(object):
    """
    a gerocoder that gets locations from the filesystem
    """

    def __init__(self):
        self.file_path = FILE_GEOCODER_PATH

        self.google = GoogleGeocoder()

        self.data = dict()
        self._load_data()

    def _load_data(self):
        """
        load all data from the file into memory
        """
        with open(self.file_path, "r") as f:
            json_data = json.load(f)
            for key, loc_pic in json_data.iteritems():
                self.data[key] = pickle.loads(loc_pic)

    def __getitem__(self, key):
        """
        return a location object for the key

        :param key: name of the city to look for

        :return Location: location matching the string searched or None
        """
        return self._get_location_from_name(key)

    def _get_location_from_name(self, key):
        """
        Get a Location object for a given key
        """
        if key in self.data:
            return self.data[key]
        else:
            raise LocationNotFoundError()

    def new_location(self, key):
        """
        look up a location on google and save it to the file
        """
        loc = self.google[key]

        self._save_location(key, loc)

    def _save_location(self, key, location):
        """
        save a location object into the file in the proper format

        :param location: location object to save
        """
        try:
            val = pickle.dumps(location)
            val = val.encode('utf8')
            self.data[key] = val
        except UnicodeDecodeError:
            print "===="
            print "cant deal with: %s" % key
            print "===="

    def commit_to_file(self):
        """
        commit all the pending changes to the file
        """   
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, sort_keys=True, indent=2)