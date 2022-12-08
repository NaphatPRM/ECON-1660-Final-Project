import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import distance

# The part is the dataset, so remove when we want to do the real one:
df = [['221 4th St, San Francisco, CA 94103', '3223 Ortega St, San Francisco, CA 94122'],
      ['2025 Hamilton Ave, San Jose, CA 95125', '488 S Almaden Ave, San Jose, CA 95110'],
      ['3720 Stephen M White Dr, San Pedro, CA 90731', '500 Sea World Dr, San Diego, CA 92109'],
      ['1010 Pearl St #7B, La Jolla, CA 92037', '19000 NE Sandy Blvd, Portland, OR 97230']]
df = pd.DataFrame(df, columns=['Address1', 'Address2'])


# Using the geocoder to find the exact place
def distanceDetermine(firstPlace, secondPlace):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(firstPlace)
    location2 = geolocator.geocode(secondPlace)
    if location is None:
        location = geolocator.geocode(firstPlace.split(",")[1] + ", BOSTON")
    elif "MEDORD" in firstPlace:
        location = geolocator.geocode(firstPlace.split(",")[0] + ", MEDFORD")
    if location2 is None:
        location2 = geolocator.geocode(secondPlace.split(",")[1] + ", BOSTON")
    elif "MEDORD" in secondPlace:
        location2 = geolocator.geocode(secondPlace.split(",")[0] + ", MEDFORD")
    if location is None or location2 is None:
        print(firstPlace)
        print(secondPlace)
    return float(distance((location.latitude, location.longitude), (location2.latitude, location2.longitude)).km)


print(distanceDetermine("4105 SW NATIVESTONE ST, BENTONVILLE", "55 NEW DUDLEY, ROXBURY"))
