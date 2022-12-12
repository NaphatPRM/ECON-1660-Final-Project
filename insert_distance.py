import socket

import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import distance

# The part is the dataset, so remove when we want to do the real one:
from urllib3.exceptions import ReadTimeoutError


# Using the geocoder to find the exact place
def distanceDetermine(firstPlace, secondPlace):
    # print(firstPlace)
    geolocator = Nominatim(user_agent="myGeocoder")
    for element in ["PRINCETON", "PRESCOTT", "TRENTON", "CHELSEA", "WEBSTER", "MARION",
                    "CONDOR", "ORLEANS", "FRANKFORT", "SHELBY"]:
        if element in firstPlace:
            firstPlace = "EAST BOSTON"
    if "FRANKLIN" in firstPlace:
        firstPlace = "TOWN OF FRANKLIN, BOSTON"
    elif "DERBY" in firstPlace:
        firstPlace = "DERBY ST, WORCHESTER"
    for element in ["BROOKLYN", "MORRISTOWN"]:
        if element in secondPlace:
            secondPlace = element + ", BOSTON"
    try:
        location = geolocator.geocode(firstPlace)
    except ReadTimeoutError:
        location = geolocator.geocode(firstPlace.split(", ")[1].strip() + ", BOSTON")
    location2 = geolocator.geocode(secondPlace)
    if location is None:
        location = geolocator.geocode(firstPlace.split(", ")[1].strip() + ", BOSTON")
    elif "MEDORD" in firstPlace:
        location = geolocator.geocode(firstPlace.split(", ")[0].strip() + ", MEDFORD")
    if location2 is None:
        location2 = geolocator.geocode(secondPlace.split(", ")[1].strip() + ", BOSTON")
    if location is None:
        return None
    # print(location)
    return float(distance((location.latitude, location.longitude), (location2.latitude, location2.longitude)).km)


# print(distanceDetermine("PARK AV, MORRISTOWN", "55 NEW DUDLEY, ROXBURY"))
