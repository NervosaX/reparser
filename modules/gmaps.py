import time
from math import radians, cos, sin, asin, sqrt
from googlemaps import GoogleMaps, GoogleMapsError

"""
Any function related to using google maps
"""
class GMaps:

    """
    @max_attempts:
        Amount of attempts that can be made on any google gmaps
        function call
    """
    def __init__(self, max_attempts=2):
        self.max_attempts = max_attempts

    """
    Stolen from http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    with no remorse. Returns distance between two GPS points.
    """
    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        km = 6367 * c
        return km

    """
    Returns distances between an address and any nearby railways

    @address:
        The address to locally check against in the form of
        a string

    @max_distance:
        Maximum distance a railway can be before being excluded
        from the return result

    @retry_wait:
        The amount of time in seconds before retrying a gmaps
        parse
    """
    def get_distance_from_railways(self, address, max_distance=3, retry_wait=1):
        print "... ... Getting GMaps Details"
        attempts = 0
        results = []

        while (True):
            gmaps = GoogleMaps()

            try:
                lat, lng = gmaps.address_to_latlng(address)
                local_search = gmaps.local_search('railway near ' + address)
            except GoogleMapsError:
                # Some sort of error occurred! Either the address is malformed,
                # or the server is having some sort of issue. We'll wait a little bit
                # and try again
                if attempts < self.max_attempts:
                    attempts += 1
                    # Wait 1 seconds before trying again
                    time.sleep(retry_wait)
                    print "Failed to parse the address. Trying again. Attempt #", attempts
                    continue
                else:
                    return None            

            # Get our results
            for result in local_search['responseData']['results']:
                
                # Probably not accurate over this point... Weird things
                # can get in
                if int(result['accuracy']) > 5:
                    continue

                distance = self.haversine(lng, lat, 
                    float(result["lng"]), float(result["lat"]))

                data = {
                    'line_name': result['titleNoFormatting'],
                    'distance': round(distance, 2)
                }

                if (distance < max_distance):
                    results.append(data)

            return results
    
    def get_travel_time_between(self, address1, address2):
        gmaps = GoogleMaps()
        try:
            directions = gmaps.directions(address1, address2)
        except GoogleMapsError:
            return None

        if directions:
            try:
                return directions["Directions"]["summaryHtml"]
            except AttributeError:
                return None