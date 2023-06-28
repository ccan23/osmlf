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
from overpass_calculations import calculations

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

    def landuse(self) -> dict:
        """
        Retrieves and returns landuse information about the location from the Overpass API.

        The method:
            - Initializes an Overpass query for landuse information.
            - Executes the Overpass query and saves the response.
            - Calculates the area for each landuse type.
            - Returns a dictionary with the landuse response and the areas of each landuse type.

        Returns:
            dict: A dictionary containing:
                - 'response': the raw response from the Overpass API.
                - 'forest', 'residential', 'commercial', 'industrial', 'farming': 
                dictionaries for each landuse type containing way features, count of ways, and total area.
        """

        # Initialize the Overpass query for landuse information, specifically targeting areas of 'forest', 'residential', 
        # 'commercial', 'industrial', and 'farming' land use types
        query = queries.generate_osm_query(
            osm_id=self.osm_id,
            key='landuse', 
            values=['forest', 'residential', 'commercial', 'industrial', 'farming']
        )

        # Execute the Overpass query and save the response
        landuse = self.api.query(query)

        # Helper lambda functions for readability: 
        # 'landuse_key' filters ways by a specific land use key
        # 'area' calculates the area of ways corresponding to a specific land use key
        landuse_key = lambda key: operations.filter_ways(landuse.ways, 'landuse', key)
        area        = lambda key: calculations.area_of_ways(landuse_key(key), self.utm_zone)

        # Return a dictionary with the landuse response and the areas of each landuse type
        return {
            'response'   : landuse,
            'forest'     : area('forest'),
            'residential': area('residential'),
            'commercial' : area('commercial'),
            'industrial' : area('industrial'),
            'farming'    : area('farming')
        }

    def leisure(self) -> dict:
        """
        Retrieves and returns leisure information about the location from the Overpass API.

        The method:
            - Initializes an Overpass query for leisure information.
            - Executes the Overpass query and saves the response.
            - Calculates the area for each leisure type.
            - Returns a dictionary with the leisure response and the areas of each leisure type.

        Returns:
            dict: A dictionary containing:
                - 'response': the raw response from the Overpass API.
                - 'marina', 'garden', 'park', 'playground', 'stadium': 
                dictionaries for each leisure type containing way features, count of ways, and total area.
        """
        
        # Initialize the overpass query for leisure information
        query = queries.generate_osm_query(
            osm_id=self.osm_id,
            key='leisure',
            values=['marina', 'garden', 'park', 'playground', 'stadium']
        )

        # Execute the Overpass query and save the response
        leisure = self.api.query(query)

        # Helper lambda functions for readability:
        # 'leisure_key' filters ways by a specific leisure key
        # 'area' calculates the area of ways corresponding to a specific leisure key
        leisure_key = lambda key: operations.filter_ways(leisure.ways, 'leisure', key)
        area        = lambda key: calculations.area_of_ways(leisure_key(key), self.utm_zone)

        # Return a dictionary with the leisure response and the areas and distances of each leisure type
        return {
            'response'      : leisure,
            'marina'        : area('marina'),
            'garden'        : area('garden'),
            'park'          : area('park'),
            'playground'    : area('playground'),
            'stadium'       : area('stadium')
        }