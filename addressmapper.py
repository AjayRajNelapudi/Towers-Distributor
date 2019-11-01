import google
import googleapiclient
import google_auth_httplib2
import numpy as np

class AddressMapper:
    '''
    AddressMapper uses google maps geolocation API to map between address string and geo-coordinates
    '''
    def __init__(self):
        pass

    def address_to_coordinates(self):
        '''
        Converts the given address in string format to its respective geo-coordinates
        :return: tuple (latitude, longitude)
        '''
        pass

    def coordinates_to_address(self):
        '''
        Converts the given geo-coordinates to its respective address in string format
        :return: address string
        '''
        pass