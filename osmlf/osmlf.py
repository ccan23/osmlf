#!/usr/bin/env python3

# The following are keys provided by OpenStreetMap (OSM). Each link is a reference to the official OSM Wiki.
# Amenities: https://wiki.openstreetmap.org/wiki/Key:amenity
# Landuse  : https://wiki.openstreetmap.org/wiki/Key:landuse
# Leisure  : https://wiki.openstreetmap.org/wiki/Key:leisure
# Tourism  : https://wiki.openstreetmap.org/wiki/Key:tourism
# Natural  : https://wiki.openstreetmap.org/wiki/Key:natural
# Highway  : https://wiki.openstreetmap.org/wiki/Key:highway
# Railway  : https://wiki.openstreetmap.org/wiki/Key:railway
# Waterway : https://wiki.openstreetmap.org/wiki/Key:waterway

# Importing the overpass API and Nominatim for geographical queries and operations
import overpy
from geopy.geocoders import Nominatim

# OMSLF Modules
from overpass_queries import queries
from overpass_operations import operations

class osmlf:

    def __init__(self, location: str):
        """
        Initializes an osmlf object by:
            - Retrieving geographical data about the specified location using geopy's Nominatim service.
            - Saving the OpenStreetMap ID of the location.
            - Initializing an Overpass API client.
            - Determining the UTM (Universal Transverse Mercator) zone based on the latitude and longitude of the location.

        Args:
            location (str): A string representing the location to gather information about.
        """
        # Geographical information about the specified location is obtained using geopy's Nominatim service
        self.location = Nominatim(user_agent='osmlf').geocode(location, featuretype='relation')

        # Save the OpenStreetMap ID of the given location
        self.osm_id = self.location.raw['osm_id']

        # Initialize the Overpass API client
        self.api = overpy.Overpass()

        # Determine the UTM zone for the given latitude and longitude
        self.utm_zone = operations.select_utm_zone(
            lat=float(self.location.raw['lat']),
            lon=float(self.location.raw['lon'])
        )

    def administrative(self) -> dict:
        """
        Retrieves and returns administrative information about the location from the Overpass API.

        The method:
            - Initializes an Overpass query for administrative information.
            - Executes the Overpass query and saves the response.
            - Returns a dictionary with the administrative response, the location's core coordinates, 
              its subareas, and its total area.

        Returns:
            dict: A dictionary containing:
                - 'response': the raw response from the Overpass API.
                - 'core': a tuple of the core (downtown) coordinates of the location (latitude, longitude).
                - 'subareas': the subareas of the location.
                - 'total_area': the total area of the location in the UTM zone (km square).
        """
        # Initialize the Overpass query for administrative information
        query = queries.administrative(osm_id=self.osm_id)

        # Execute the Overpass query and save the response        
        admin = self.api.query(query)

        # Return a dictionary with the administrative information, core coordinates, subareas, and total area
        return {
            'response'  : admin,
            'core'      : (float(self.location.raw['lat']), float(self.location.raw['lon'])), 
            'subareas'  : operations.subareas(relations=admin.relations),
            'total_area': operations.total_area(relations=admin.relations, utm_zone=self.utm_zone)
        }
