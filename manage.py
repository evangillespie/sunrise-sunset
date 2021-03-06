# !/bin/

from src.sunsetter import SunSetter
from src.config import FILE_GEOCODER_PATH, SPLIT_FLAP_NUMBER_OF_CHARCTERS
from src.enums import ALL_CITY_NAMES
from src.geocoder import FileGeocoder
from src.exceptions import LocationNotFoundError
from astral import AstralError
from sys import argv
from time import sleep
import random
import sys
import serial

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
        if (s.get_current_datetime() - s.date).days > 0:
            print "refreshing the date"
            s.refresh_date()

        cities = s.find_rise_or_set_at_time(
            interval=interval,
            rise_or_set=rise_or_set
        )

        city = s.pick_one_city(cities)

        _print_city(city)
        sleep(interval)

def run_split_flap_loop(rise_or_set='sunrise', interval=60):
    """
    run an infinite loop and display the closest sunset and sunrise every <interval> seconds
    Send the output to an arduino (by serial) which controls a split flap display

    :rise_or_set: 'sunrise' or 'sunset' depending on which one you're looking to find
    :param interval: number of seconds between each check
    """
    num_letters = SPLIT_FLAP_NUMBER_OF_CHARCTERS #number of split flap letters that exist
    ser = _get_serial_connection()

    s = SunSetter()
    while True:
        try:
            if (s.get_current_datetime() - s.date).days > 0:
                print "refreshing the date"
                s.refresh_date()

            cities = s.find_rise_or_set_at_time(
                interval=interval,
                rise_or_set=rise_or_set
            )
            city = s.pick_one_city(cities)

            _print_city(city)
            _send_city_by_serial(ser, city[:num_letters].ljust(num_letters))

            sleep(interval)
        except KeyboardInterrupt:
            break
    print "Peace out."

def _print_city(city):
    if city:
        print city
    else:
        print "-"


def _send_city_by_serial(ser, city):
    """
    send the city name to the arduino via serial

    :param ser: serial connection
    :param city: city name (string)
    """
    city = city.lower()
    ser.write(city)


def _get_serial_connection():
    """
    return a serial connection to the arduino
    """
    # @TODO: try to connect on the other port if this conection fails
    return serial.Serial('/dev/ttyACM0', 9600)


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


def load_test_split_flap(delay=15):
    """
    cycle through tonnes of cities on the split flap to load test it

    :param delay: time to wait between city changes(seconds)
    """
    def repeat_to_length(string, length):
        """
        repeat a given string until it is as long as length
        """
        string = string + " "
        return (string * ((length/len(string))+1))[:length]

    print "loading cities..."
    cities = []
    for city_list in ALL_CITY_NAMES.values():
        cities += city_list
    print "establishing connection"

    ser = _get_serial_connection()
    sleep(5)
    num_letters = SPLIT_FLAP_NUMBER_OF_CHARCTERS

    counter = 1
    while True:
        try:
            city = random.choice(cities)
            print "%.3d: %s" % (counter, city)
            
            city = repeat_to_length(city, SPLIT_FLAP_NUMBER_OF_CHARCTERS)

            _send_city_by_serial(ser, city[:num_letters].ljust(num_letters))

            counter += 1
            sleep(delay)
        except KeyboardInterrupt:
            break

    print "Load test complete."


def simulate_24_hours(rise_or_set, time_to_simulate):
    """
    simulate a 24 hour period, finding a sunrise/sunset every minute

    :param rise_or_set: 'sunrise' or 'sunset'
    :param time_to_simulate: the length of the simulation (in hours)
    """
    if (rise_or_set != 'sunrise') and (rise_or_set != 'sunset'):
        raise Exception("you need to specify 'sunrise' or 'sunset'")

    time_interval = 60
    s = SunSetter()

    time = s.get_current_time()
    for i in range(time_to_simulate * 60 * 60 / time_interval):  # one for each minute in the day
        cities = s.find_rise_or_set_at_time(time_interval, rise_or_set, time)
        _print_city(s.pick_one_city(cities))
        
        time.increment_time(time_interval)

def print_help():
    print "USAGE: %s <command>" % argv[0]
    print "COMMANDS:"
    print "store_locations: save all locations for offline use"
    print "run_cli <sunrise/sunset> <interval=60>: run the infinite looping program on this computer"
    print "run_split_flap <sunrise/sunset> <interval=60>: run the infinite looping program using the split flap display"
    print "times: show a list of all sunset or sunrise times"
    print "load_test_split_flap: load test the split flap"
    print "simulate_24_hours: simulate a 24 hour cycle <sunrise/sunset> <length of silumation (hours)>"

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

        elif command == 'load_test_split_flap':
            load_test_split_flap()

        elif command == 'simulate_24_hours':
            if len(argv) < 3:
                print "You're missing the sunrise/sunset param"
                print "EG. python manage.py simulate_24_hours sunrise"
            else:
                if len(argv) >= 4:
                    sim_time = argv[3]
                else:
                    sim_time = 24
                simulate_24_hours(argv[2], int(sim_time))

        else:
            print_help()
    else:
        print_help()
