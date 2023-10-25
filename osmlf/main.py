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
from .overpass_queries import queries
from .overpass_operations import operations
from .overpass_calculations import calculations

class osmlf:

    __version__ = '0.0.1'

    def __init__(self, location):
        """
        Initializes an osmlf object with the specified location.

        Args:
            location: The name or address of the location.

        The method performs the following tasks:
            - Geocodes the location using Nominatim to obtain the corresponding OpenStreetMap relation.
            - Extracts the OpenStreetMap ID from the geocoding result.
            - Initializes an Overpass API object.
            - Determines the UTM zone for the location based on its latitude and longitude.
            - Sets default values for different OSM key categories.

        Note:
            The OpenStreetMap relation ID is used to retrieve detailed information about the location.
        """
        # Geocode the location using Nominatim to obtain the OpenStreetMap relation   
        self.location = Nominatim(user_agent='osmlf').geocode(location, featuretype='relation', extratags=True)

        # Check if geocode location is valid, set the ok attribute to True
        if self.location:

            self.ok = True

            # Extract the OpenStreetMap ID from the geocoding result
            self.osm_id = self.location.raw['osm_id']

            # Initialize an Overpass API object
            self.api = overpy.Overpass()

            # Determine the UTM zone for the location based on its latitude and longitude
            self.utm_zone = operations.select_utm_zone(
                lat=float(self.location.raw['lat']),
                lon=float(self.location.raw['lon'])
            )

            # Set default values for different OSM key categories
            self.default_values = {
                'amenity': [
                    'bar', 'cafe', 'fast_food', 'food_court', 'pub', 'restaurant',
                    'college', 'library', 'school', 'university', 'atm', 'bank',
                    'clinic', 'dentist', 'doctors', 'hospital', 'pharmacy', 'veterinary',
                    'cinema', 'conference_centre', 'theatre', 'courthouse', 'fire_station',
                    'police', 'post_office', 'townhall', 'marketplace', 'grave_yard', 'place_of_worship'
                ],
                'landuse': ['forest', 'residential', 'commercial', 'industrial', 'farming'],
                'leisure': ['marina', 'garden', 'park', 'playground', 'stadium'],
                'tourism': [
                    'aquarium', 'artwork', 'attraction', 'hostel', 'hotel', 
                    'motel', 'museum', 'theme_park', 'viewpoint', 'zoo'
                ],
                'natural': ['beach'],
                'highway': [],
                'railway': ['platform', 'station', 'stop_area'],
                'waterway': []
            }
        
        # If geocode location is not valid, set the ok attribute to False
        else:
            self.ok = False
    
    def __str__(self) -> str:
        return self.location.__str__()
    
    def __repr__(self) -> str:
        return f'osmlf({self.location.__str__()})'
    
    def __objects(self, key: str, values: list) -> dict:
        """
        Retrieves OSM objects (nodes and ways) from the Overpass API based on the specified key-value pairs
        and organizes them into a dictionary.

        Args:
            key (str): The key to filter the OSM objects.
            values (list): A list of values to filter the OSM objects.

        Returns:
            dict: A dictionary containing the retrieved OSM objects, grouped by their respective values.
                The dictionary has two keys: 'nodes' and 'ways'.
                Each key maps to a dictionary where the keys are the OSM object values and the values
                are lists of OSM object features (nodes or ways) associated with that value.
        """
        # Generate the Overpass query for OSM object information
        query = queries.generate_osm_query(self.osm_id, key, values)

        # Execute the Overpass query and save the response
        response = self.api.query(query)

        # Retrieve nodes for each value of the key and store them in a dictionary
        nodes = {value: calculations.nodes(operations.filter_nodes(response.nodes, key, value)) for value in values}

        # Retrieve ways for each value of the key and store them in a dictionary
        ways = {value: calculations.ways(operations.filter_ways(response.ways, key, value), self.utm_zone) for value in values}

        # Return the dictionary containing nodes and ways grouped by key values
        return {'nodes': nodes, 'ways': ways}

    def __lengths(self, key: str, values: list) -> dict:
        """
        Retrieves road lengths based on the specified key and values from the Overpass API response.

        The method generates an Overpass query to fetch the OSM objects that match the given key and values.
        It executes the query, processes the response, and extracts the road lengths for each matching object.
        The resulting dictionary contains the total length of roads and a list of road features, each with its tags, coordinates, and length.

        Args:
            key (str): The key for the OSM object to retrieve (e.g., 'highway').
            values (list): A list of values to filter the OSM objects by.

        Returns:
            dict: A dictionary containing:
                - 'total_length' (float): The total length of all roads that match the specified key and values.
                - 'info' (list): A list of dictionaries representing road features, with the following keys:
                    - 'tags' (dict): Tags associated with the road feature.
                    - 'coordinates' (list): A list of coordinate tuples representing the geometry of the road feature.
                    - 'length' (float): The length of the road feature in kilometers.
        """
        # Generate the Overpass query for OSM object information
        query = queries.generate_osm_query(self.osm_id, key, values)

        # Execute the overpass query and save the response
        response = self.api.query(query)

        # Process the response to extract key information
        length = [
            {
                'tags'       : way.tags,
                'coordinates': [(float(node.lat), float(node.lon)) for node in way.nodes],
                'length'     : calculations.total_distance(
                    [(float(node.lat), float(node.lon)) for node in way.nodes],
                    self.utm_zone
                )
            } for way in response.ways
        ]

        # Return the dictionary containing lengths of roads
        return {
            'total_length': sum([elem['length'] for elem in length]),
            'info'        : length
        }
    
    def __execute(self, target: str, key: str, values):
        
        # If values is None, use the default values
        if values is None:
            values = self.default_values[key]
        
        # If values is a string, convert it to a single-element list
        elif values is not None and isinstance(values, str):
            values = [values]

        # If target is objects (nodes and ways)
        if target == 'objects':
            # Call the __objects method to retrieve and return the target objects
            return self.__objects(key, values)

        # If target is lengths (lengts of roads (highway and waterway))
        elif target == 'lengths':
            return self.__lengths(key, values)

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
            'core'      : (float(self.location.raw['lat']), float(self.location.raw['lon'])), 
            'subareas'  : operations.subareas(self.osm_id),
            'total_area': operations.total_area(relations=admin.relations, utm_zone=self.utm_zone),
            'extratags' : self.location.raw['extratags'],
            'osm_url'   : f'https://www.openstreetmap.org/relation/{self.osm_id}'
        }
    
    def amenity(self, values=None) -> dict:
        """
        Retrieves amenity information about the location from the Overpass API.

        Args:
            values (list or str): A list of values or a single value to filter the OSM objects.
                If None, it retrieves amenity objects using the default values.
                Possible values can be found at https://wiki.openstreetmap.org/wiki/Key:amenity

        Returns:
            dict: A dictionary containing the retrieved OSM objects, grouped by their respective values.
        """
        return self.__execute(target='objects', key='amenity', values=values)
    
    def landuse(self, values=None) -> dict:
        """
         Retrieves landuse information about the location from the Overpass API.

        Args:
            values (list or str): A list of values or a single value to filter the OSM objects.
                If None, it retrieves landuse objects using the default values.
                Possible values can be found at https://wiki.openstreetmap.org/wiki/Key:landuse

        Returns:
            dict: A dictionary containing the retrieved OSM objects, grouped by their respective values.
        """
        return self.__execute(target='objects', key='landuse', values=values)
    
    def leisure(self, values=None) -> dict:
        """
        Retrieves leisure information about the location from the Overpass API.

        Args:
            values (list or str): A list of values or a single value to filter the OSM objects.
                If None, it retrieves leisure objects using the default values.
                Possible values can be found at https://wiki.openstreetmap.org/wiki/Key:leisure

        Returns:
            dict: A dictionary containing the retrieved OSM objects, grouped by their respective values.
        """
        return self.__execute(target='objects', key='leisure', values=values)
    
    def tourism(self, values=None) -> dict:
        """
        Retrieves tourism information about the location from the Overpass API.

        Args:
            values (list or str): A list of values or a single value to filter the OSM objects.
                If None, it retrieves tourism objects using the default values.
                Possible values can be found at https://wiki.openstreetmap.org/wiki/Key:tourism

        Returns:
            dict: A dictionary containing the retrieved OSM objects, grouped by their respective values.
        """
        return self.__execute(target='objects', key='tourism', values=values)
    
    def natural(self, values=None) -> dict:
        """
        Retrieves natural information about the location from the Overpass API.

        Args:
            values (list or str): A list of values or a single value to filter the OSM objects.
                If None, it retrieves natural objects using the default values.
                Possible values can be found at https://wiki.openstreetmap.org/wiki/Key:natural

        Returns:
            dict: A dictionary containing the retrieved OSM objects, grouped by their respective values.
        """
        return self.__execute(target='objects', key='natural', values=values)
    
    def highway(self, values=None) -> dict:
        """
        Retrieves highway information about the location from the Overpass API.

        Args:
            values (list or str): A list of values or a single value to filter the OSM objects.
                If None, it retrieves highway objects using the default values.
                Possible values can be found at https://wiki.openstreetmap.org/wiki/Key:highway

        Returns:
            dict: A dictionary containing the retrieved OSM objects, grouped by their respective values.
        """
        return self.__execute(target='lengths', key='highway', values=values)
    
    def railway(self, values=None) -> dict:
        """
        Retrieves railway information about the location from the Overpass API.

        Args:
            values (list or str): A list of values or a single value to filter the OSM objects.
                If None, it retrieves railway objects using the default values.
                Possible values can be found at https://wiki.openstreetmap.org/wiki/Key:railway

        Returns:
            dict: A dictionary containing the retrieved OSM objects, grouped by their respective values.
        """
        return self.__execute(target='objects', key='railway', values=values)
    
    def waterway(self, values=None) -> dict:
        """
        Retrieves waterway information about the location from the Overpass API.

        Args:
            values (list or str): A list of values or a single value to filter the OSM objects.
                If None, it retrieves waterway objects using the default values.
                Possible values can be found at https://wiki.openstreetmap.org/wiki/Key:waterway

        Returns:
            dict: A dictionary containing the retrieved OSM objects, grouped by their respective values.
        """
        return self.__execute(target='objects', key='waterway', values=values)
    
