# !/bin/

from src.enums import FILE_GEOCODER_PATH, ALL_CITY_NAMES
from src.geocoder import FileGeocoder
from src.exceptions import LocationNotFoundError
from astral import AstralError
from optparse import OptionParser
from sys import argv

__author__ = ('evan', )

def populate_file_geocoder():
    """
    populate the filesystem geocoder using information from the google geocoder
    geta location for every place in ALL_CITY_NAMES, if possible
    """
    file_geo = FileGeocoder()
    try:
        for region, cities in ALL_CITY_NAMES.iteritems():
            for city in cities:
                try:
                    file_geo.new_location(city)
                except LocationNotFoundError:
                    print "CANT FIND CITY: %s" % city

        file_geo.commit_to_file()
        
    except AstralError as e:
        print "ASTRAL ERROR: %s" % e

def run_loop(interval=60):
    """
    run an infinite loop and display the closest sunset and sunrise every <interval> seconds
    
    :param interval: number of seconds between each check
    """
    while True:
        print "in the loop"


def print_help():
    print "USAGE: %s <command>" % argv[0]
    print "COMMANDS:"
    print "store_locations: save all locations for offline use"
    print "run: run the infinite looping program"
    print "times: show a list of all sunset and sunrise times, in order"

if __name__ == '__main__':
    if len(argv) >= 2:
        command = argv[1]
        if command == 'store_locations':
            populate_file_geocoder()
        elif command == 'run':
            run_loop()
        elif command == 'times':
            # TODO: implement
            raise NotImplementedError()
        else:
            print_help()
    else:
        print_help()