# !/bin/

from src.sunsetter import SunSetter
from src.enums import FILE_GEOCODER_PATH, ALL_CITY_NAMES, SOME_CITY_NAMES
from src.geocoder import FileGeocoder
from src.exceptions import LocationNotFoundError
from astral import AstralError
from optparse import OptionParser
from sys import argv
from time import sleep

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
                    sleep(0.1)
                except LocationNotFoundError:
                    print "CANT FIND CITY: %s" % city
                except ValueError as e:
                    print "%s" % e

        file_geo.commit_to_file()
        
    except AstralError as e:
        print "ASTRAL ERROR: %s" % e
        print "maybe cant access google maps api"
        file_geo.commit_to_file()

def run_loop(interval=60):
    """
    run an infinite loop and display the closest sunset and sunrise every <interval> seconds
    
    :param interval: number of seconds between each check
    """
    while True:
        # TODO: implement properly
        print "in the loop. Implement me properly"
        sleep(interval)

def show_all_times(rise_or_set):
    """
    show time sunrise or sunset time for every city
    prints to stdout

    :param rise_or_set: 'sunset' or 'sunrise'
    """
    if rise_or_set == 'rise':
        rise_or_set = 'sunrise'
    if rise_or_set == 'set':
        rise_or_set = 'sunset'
        
    if rise_or_set != 'sunset' and rise_or_set != 'sunrise':
        print "invalid rise_or_set: %s" % rise_or_set
        return

    print "Showing the time for all %ss" % rise_or_set
    # TODO: implement
    s = SunSetter()
    times = s.get_all_times()
    for city, times in times.iteritems():
        print "%s\t%s" % (city, times[rise_or_set])

def print_help():
    print "USAGE: %s <command>" % argv[0]
    print "COMMANDS:"
    print "store_locations: save all locations for offline use"
    print "run: run the infinite looping program"
    print "times: show a list of all sunset or sunrise times"

if __name__ == '__main__':
    if len(argv) >= 2:
        command = argv[1]
        if command == 'store_locations':
            populate_file_geocoder()
        elif command == 'run':
            run_loop()
        elif command == 'times':
            if len(argv) < 3:
                print "You're missing the sunrise/sunset param"
                print "EG. python manage.py times sunrise"
            else:
                show_all_times(argv[2])
        else:
            print_help()
    else:
        print_help()