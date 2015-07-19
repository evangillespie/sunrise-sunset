# !/bin/

from src.sunsetter import SunSetter
from src.enums import FILE_GEOCODER_PATH, ALL_CITY_NAMES, SOME_CITY_NAMES
from src.geocoder import FileGeocoder
from src.exceptions import LocationNotFoundError
from astral import AstralError
from sys import argv
from time import sleep
import random
import sys

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


def run_cli_loop(rise_or_set='sunrise', interval=60):
    """
    run an infinite loop and display the closest sunset and sunrise every <interval> seconds
    write to standard out

    :rise_or_set: 'sunrise' or 'sunset' depending on which one you're looking to find
    :param interval: number of seconds between each check
    """
    s = SunSetter()
    while True:
        cities = s.find_rise_or_set_at_time(
            interval=interval,
            rise_or_set=rise_or_set
        )

        if cities:
            city = random.choice(cities)
        else:
            city = None

        _print_city(rise_or_set, city)
        sleep(interval)

def run_split_flap_loop(rise_or_set='sunrise', interval=60):
    """
    run an infinite loop and display the closest sunset and sunrise every <interval> seconds
    Send the output to an arduino (by serial) which controls a split flap display

    :rise_or_set: 'sunrise' or 'sunset' depending on which one you're looking to find
    :param interval: number of seconds between each check
    """
    import serial

    num_letters = 5 #number of split flap letters that exist
    ser = serial.Serial('/dev/ttyACM0', 9600)

    s = SunSetter()
    while True:
        cities = s.find_rise_or_set_at_time(
            interval=interval,
            rise_or_set=rise_or_set
        )
        if cities:
            city = random.choice(cities)
        else:
            city = ''

        _send_city_by_serial(ser, city[:num_letters].ljust(num_letters))
        
        sleep(interval)


def _print_city(rise_or_set, city):
    if city:
        # pick a random city from the list
        print city
    else:
        # there are no cities right now
        print "-"


def _send_city_by_serial(ser, city):
    """
    send the city name to the arduino via serial

    :param ser: serial connection
    :param city: city name (string)
    """
    ser.write(city)


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

    s = SunSetter()

    print "Current time is %s" % s.get_current_time()
    print "Showing the time for all %ss" % rise_or_set
    times = s.get_all_times()
    for city, times in times.iteritems():
        print "%s\t%s" % (city, times[rise_or_set])


def print_help():
    print "USAGE: %s <command>" % argv[0]
    print "COMMANDS:"
    print "store_locations: save all locations for offline use"
    print "run_cli <sunrise/sunset> <interval=60>: run the infinite looping program on this computer"
    print "run_split_flap <sunrise/sunset> <interval=60>: run the infinite looping program using the split flap display"
    print "times: show a list of all sunset or sunrise times"

if __name__ == '__main__':
    if len(argv) >= 2:
        command = argv[1]
        if command == 'store_locations':
            populate_file_geocoder()
        elif command == 'run_cli':
            if len(argv) >= 3:
                rise_or_set = argv[2]
                if rise_or_set != 'sunrise' and rise_or_set != 'sunset':
                    print "you trying to get a sunrise or sunset?"
                    print_help()
                    sys.exit()
                if len(argv) == 4:
                    interval = int(argv[3])
                else:
                    interval = 60

                run_cli_loop(rise_or_set, interval)

            else:
                print_help()

        elif command == 'run_split_flap':
            if len(argv) >= 3:
                rise_or_set = argv[2]
                if rise_or_set != 'sunrise' and rise_or_set != 'sunset':
                    print "you trying to get a sunrise or sunset?"
                    print_help()
                    sys.exit()
                if len(argv) == 4:
                    interval = int(argv[3])
                else:
                    interval = 60

                run_split_flap_loop(rise_or_set, interval)

            else:
                print_help()


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
