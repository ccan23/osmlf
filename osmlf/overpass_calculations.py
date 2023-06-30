#!/usr/bin/env python3

# Area calculations
from pyproj import Transformer
from shapely.geometry import Polygon

# Distance
from geopy.distance import geodesic

class calculations:

    def nodes(nodes: list) -> dict:
        """
        Retrieves specific information from a list of OSM nodes and returns a list of dictionaries with the desired data.

        Args:
            nodes (list): A list of OSM node objects.

        Returns:
            list: A list of dictionaries containing the desired information for each node.
        """

        # Create a list of dictionaries with specific information extracted from each node object
        return [{'id': node.id, 'tags': node.tags, 'coordinate': (float(node.lat), float(node.lon))} for node in nodes]

    def ways(ways: list, utm_zone: str) -> dict:
        """
        Processes a list of OpenStreetMap (OSM) ways and extracts relevant features, including their area.

        Args:
            ways (list): A list of OSM way objects.
            utm_zone (str): The UTM zone for which to compute the area.

        Returns:
            dict: A dictionary containing features of each way, total way count, and the total area.

        Note: 
            The function calculates the area of each way by projecting its coordinates from the WGS84 
            coordinate system to the specified UTM zone. It then extracts the ID, name, original coordinates, 
            and computed area for each way. The area is provided in square kilometers.
        """

        # Initialize a Transformer object for converting the coordinates from WGS84 to the specified UTM zone
        transformer = Transformer.from_crs('EPSG:4326', utm_zone, always_xy=True)

        # Initialize an empty dictionary to store the features of each way
        way_features = {'ways': list()}

        # Process each way in the list
        for way in ways:

            # Extract the coordinates of the way's nodes
            coordinates = [(float(node.lat), float(node.lon)) for node in way.nodes]

            # Extract the coordinates as pyproj wants
            coordinates_pyroj = [(float(node.lon), float(node.lat)) for node in way.nodes]

            # Project the coordinates to the specified UTM zone
            coordinates_projected = [transformer.transform(*coord) for coord in coordinates_pyroj]

            # Construct a polygon from all the projected coordinates and compute its area in square kilometers
            polygon_projected = Polygon(coordinates_projected)
            area = polygon_projected.area / 10**6

            # Store the way's ID, name, original coordinates
            way_features['ways'].append({
                'way_id'     : way.id,
                'name'       : way.tags.get('name', 'unknown'),
                'coordinates': coordinates,
                'area'       : area
            })

        # Add the total count of processed ways and the total area of all ways to the result
        way_features['way_count'] = len(way_features['ways'])
        way_features['total_area'] = sum([way['area'] for way in way_features['ways']])

        return way_features
    
    def area_of_members(members: list, utm_zone: str) -> dict:
        """
        Compute the total area of all geometries in the given OSM relation members in a specific UTM zone.
        
        This function first extracts all coordinates from the provided members. 
        It then uses the Transformer from pyproj to convert these coordinates from the WGS84 format to the given UTM zone.
        It forms a polygon from these converted coordinates and calculates its area in square kilometers.
        
        Args:
            members (list): A list of OSM relation members. Each member should have 'geometry' which should contain 'lon' and 'lat'.
            utm_zone (str): The UTM zone to be used for the area calculation. This should be a string in the format expected by pyproj.

        Returns:
            float: The total area of all the geometries, in square kilometers.
        """
    
        # Initialize a Transformer object for converting the coordinates from WGS84 to the specified UTM zone
        transformer = Transformer.from_crs('EPSG:4326', utm_zone, always_xy=True)

        # Extract all coordinates from 'outer' member geometries
        # Each tuple contains a longitude and latitude pair
        coordinates = [(float(geometry.lon), float(geometry.lat)) for member in members for geometry in member.geometry]

        # Convert the extracted WGS84 coordinates to the specified UTM zone using the transformer
        coordinates_projected = [transformer.transform(*coord) for coord in coordinates]

        # Create a Polygon using the projected coordinates
        polygon_projected = Polygon(coordinates_projected)

        # Compute the area of the created polygon and convert it to square kilometers (since the original area is in square meters)
        # Return the computed area
        return polygon_projected.area / 10**6

    def total_distances(coordinates: list) -> float:
        """This function computes the total distance of a sequence of geographical coordinates.
    
        Args:
            coordinates (list): A list of tuples where each tuple represents (latitude, longitude).

        Returns:
            float: Total distance in kilometers.
        """

        # Initialize the total distance to 0
        total_distance = 0.0
        
        # Iterate over each pair of consecutive coordinates
        for i in range(len(coordinates) - 1):

            # Add the distance between the current pair of coordinates to the total distance
            total_distance += geodesic(coordinates[i], coordinates[i + 1]).km

        return total_distance
    