from datetime import timedelta
from geopy import geocoders
from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt
import textwrap


def main():
    """
    EARTHBOUND TRAVELER
    User gives names of two cities
    Program gets lon lat of them
    Program calculates the distance in Miles using the Haversine formula.
        (The haversine formula determines the great-circle distance between two
        points on a sphere given their longitudes and latitudes. Important in navigation,
        it is a special case of a more general formula in spherical trigonometry, the law of haversines,
        that relates the sides and angles of spherical triangles.)
    Then the program calculates how long it would take to get there using different modes of travel:
    Walking at speed 3 mph
    Biking at speed 12 mph
    Driving a car at avg speed of 55mph
    Flying in a commercial plane at speed 575 mph
    Flying in a rocket at speed 17,000 mph
    """

    print('--------------------------------------')
    print('        EARTHBOUND TRAVELER')
    print('--------------------------------------')
    print()
    msg = '''This program calculates the distance of two locations anywhere around the globe in Miles using the Haversine formula. Sorry all you Flat-Earthers out there!'''
    print(textwrap.fill(msg, 80))
    print()

    msg = '''Then it displays how long it would take to get there using different modes of travel including:
    1) Walking
    2) Biking
    3) Driving a Car
    4) Taking a Commercial Jet
    5) Riding in a Rocket
    '''
    print(msg)

    # ask user for input here
    # start = 'Oslo, Norway'
    # finish = 'Vancouver, BC'


    start = input('Please enter starting city (i.e. Las Vegas, NV) ')
    pos1 = get_position(start)
    if not pos1:
        print('Sorry we cant find that location. Check with http://www.geonames.org for details.')
        print()
        input('Press ENTER to QUIT')
        return
    print()

    finish = input('Please enter destination city (i.e. Paris, France OR Bankok, China) ')
    pos2 = get_position(finish)
    if not pos2:
        print('Sorry we cant find that location. Check with http://www.geonames.org for details.')
        print()
        input('Press ENTER to QUIT')
        return
    print()

    # get distance based on the two coordinates
    dist = calc_the_dist(pos1, pos2)
    if dist < 1:
        print('Sorry the calculated distance is Zero. Are you ok?')
        print()
        input('Press ENTER to QUIT')
        return

    print()
    print('You are looking to travel about {:,} miles from {} to {}'.format(int(dist), start, finish))
    print()
    input('Press ENTER to continue...')
    print()

    # to walk there
    hrs = dist / 3
    t = timedelta(seconds=hrs * 3600)
    sec = t.total_seconds()
    answer = display_time(sec, 7)
    print('--------------------------------------------------')
    print('Walking there would take {}.'.format(answer))
    print('Provided you have a pair of comfortable shoes.')
    print('--------------------------------------------------')
    print()
    input('Press ENTER to continue...')
    print()

    # to bike there
    hrs = dist / 12  # avg mph when walking
    t = timedelta(seconds=hrs * 3600)
    sec = t.total_seconds()
    answer = display_time(sec, 7)
    print('--------------------------------------------------')
    print('Pedaling a bike would take {}.'.format(answer))
    print('But only if you have very sturdy tires.')
    print('--------------------------------------------------')
    print()
    input('Press ENTER to continue...')
    print()

    # drive there
    hrs = dist / 55  # avg mph
    t = timedelta(seconds=hrs * 3600)
    sec = t.total_seconds()
    answer = display_time(sec, 7)
    print('--------------------------------------------------')
    print('Making the trip by car would take {}.'.format(answer))
    print('Including a magical freeway for those over-the-water parts.')
    print('--------------------------------------------------')
    print()
    input('Press ENTER to continue...')
    print()

    # fly in plane
    hrs = dist / 575  # avg mph
    t = timedelta(seconds=hrs * 3600)
    sec = t.total_seconds()
    answer = display_time(sec, 7)
    print('--------------------------------------------------')
    print('Flying in a commercial jet would take {}.'.format(answer))
    print('Ignoring the wait at security of course.')
    print('--------------------------------------------------')
    print()
    input('Press ENTER to continue...')
    print()

    # by rocket
    hrs = dist / 17000  # avg mph
    t = timedelta(seconds=hrs * 3600)
    sec = t.total_seconds()
    answer = display_time(sec, 7)
    print('--------------------------------------------------')
    print('Making the trip in a SpaceX Rocket would take {}.'.format(answer))
    print('With Elon Musk''s permission.. Good luck with that.')
    print('--------------------------------------------------')
    print()
    input('Press ENTER to continue...')
    print()

    # crazy distance
    # circumference of the Earth in miles is 24,901.
    dist = 24901
    hrs = dist / 3  # avg mph
    t = timedelta(seconds=hrs * 3600)
    sec = t.total_seconds()
    answer = display_time(sec, 7)
    print('--------------------------------------------------')
    print('Fun Factoid:')
    print('Walking all the way around the circumference of the Earth(24,901 miles) would take {}.'.format(answer))
    print('Provided you are entirely insane.')
    print('--------------------------------------------------')
    print()
    print('END PROGRAM - THANK YOU FOR PLAYING.')
    print()
    print('HOW ABOUT A NICE GAME OF CHESS?')
    print()
    input('Press ENTER to QUIT')

@dataclass
class Position:
    name: str
    lon: float = 0.0
    lat: float = 0.0

    # You can add a .distance_to() method to your data class just like you can with normal classes:
    def distance_to(self, other):
        # r = 6371  # Earth radius in kilometers
        r = 3958  # rad in miles

        # The haversine formula
        lam_1, lam_2 = radians(self.lon), radians(other.lon)
        phi_1, phi_2 = radians(self.lat), radians(other.lat)
        h = (sin((phi_2 - phi_1) / 2) ** 2
             + cos(phi_1) * cos(phi_2) * sin((lam_2 - lam_1) / 2) ** 2)
        return 2 * r * asin(sqrt(h))


def get_position(source):
    gn = geocoders.GeoNames('EU', 'dwoolst')
    citi = None

    if source == '':
        return None

    g = gn.geocode(source, timeout=90)
    if g:
        citi = Position(g.address, g.longitude, g.latitude)
        addr, lon, lat = g.address, g.longitude, g.latitude
        print()
        print(f'{addr} is located at Latitude: {round(lat,2)}, Longitude: {round(lon,2)}')
    return citi


def calc_the_dist(citi1, citi2):
    # calc the distance
    dist = citi1.distance_to(citi2)
    return dist


intervals = (
    ('years', 31536000),
    ('months', 2628000),
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),  # 60 * 60 * 24
    ('hours', 3600),  # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
)


def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(int(value), name))
    return ', '.join(result[:granularity])


if __name__ == '__main__':
    main()
