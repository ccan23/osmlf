#!/usr/bin/env python3

# Keys OSM provides

# Amenities: https://wiki.openstreetmap.org/wiki/Key:amenity
# Landuse  : https://wiki.openstreetmap.org/wiki/Key:landuse
# Leisure  : https://wiki.openstreetmap.org/wiki/Key:leisure
# Tourism  : https://wiki.openstreetmap.org/wiki/Key:tourism
# Natural  : https://wiki.openstreetmap.org/wiki/Key:natural
# Highway  : https://wiki.openstreetmap.org/wiki/Key:highway
# Railway  : https://wiki.openstreetmap.org/wiki/Key:railway
# Waterway : https://wiki.openstreetmap.org/wiki/Key:waterway

# overpass API and Nominatim
import overpy
from geopy.geocoders import Nominatim

# OSMLF Modules
from overpass_queries import queries
from overpass_operations import operations

class osmlf:
    """OpenStreetMap Location Features"""

    def __init__(self, location: str):
        # Use geopy to get geographical information about the specified location
        self.location = Nominatim(user_agent='osmlf').geocode(location, featuretype='relation')

        # Save OSM ID of given location
        self.osm_id = self.location.raw['osm_id']

        # Initialize Overpass API client
        api = overpy.Overpass()

        # Determine the UTM zone for the given latitude and longitude
        self.utm_zone = operations.select_utm_zone(
            lat=float(self.location.raw['lat']),
            lon=float(self.location.raw['lon'])
        )

        # Initialize Overpass API queries as strings
        self.queries = {
            'administrative': queries.administrative(osm_id=self.osm_id)
        }

        # Initialize Overpass API queries as responses
        self.responses = {
            'administrative': api.query(self.queries['administrative'])
        }

    @property
    def administrative(self) -> dict:

        # Administrative Overpass API response
        admin = self.responses['administrative']

        # Return a dictionary with all the information
        return {
            'core'      : (float(self.location.raw['lat']), float(self.location.raw['lon'])), # Core (downtown) coordinates of the location (latitude, longitude)
            'subareas'  : operations.subareas(relations=admin.relations),
            'total_area': operations.total_area(relations=admin.relations, utm_zone=self.utm_zone)
        }
