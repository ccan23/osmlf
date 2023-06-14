#!/usr/bin/env python3

# Area calculations
from pyproj import Transformer
from shapely.geometry import Polygon

# Distance
from geopy.distance import geodesic

class calculations:
    
    def filter_members(relations: list, role: str) -> list:
        """
        This function filters members of given relations based on the specified role.
        
        Args:
            relations (list): A list of OSM relation objects.
            role (str): The role to filter members by.

        Returns:
            list: A list of reference IDs for members with the specified role.
        """

        #  Using list comprehension to find members with the specified role in all relations and return it
        return [member for relation in relations for member in relation.members if member.role == role]

    def area_of_ways(ways: list, utm_zone: str) -> dict:
        """
        This function computes the area of a list of OSM ways in a specified UTM zone.
        
        Args:
            ways (list): A list of OSM way objects.
            utm_zone (str): The UTM zone for which to compute the area.

        Returns:
            dict: A dictionary that contains way features, count of ways, and total area.

        Note: 
            The area is calculated by first projecting all the way's coordinates from the WGS84 
            coordinate system to the specified UTM zone, constructing a polygon 
            from these projected coordinates, and then computing its area. The area is in square kilometers.
        """

        # Initialize a Transformer object for converting the coordinates from WGS84 to the specified UTM zone
        transformer = Transformer.from_crs('EPSG:4326', utm_zone, always_xy=True)

        # Initialize an empty list to accumulate all projected coordinates
        all_coordinates_projected = []

        # Initialize an empty dictionary to store the features of each way
        way_features = {'ways': list()}

        # Process each way in the list
        for way in ways:

            # Extract the coordinates of the way's nodes
            coordinates = [(float(node.lon), float(node.lat)) for node in way.nodes]

            # Project the coordinates to the specified UTM zone
            coordinates_projected = [transformer.transform(*coord) for coord in coordinates]

            # Accumulate the projected coordinates
            all_coordinates_projected.extend(coordinates_projected)

            # Store the way's ID, name, original coordinates
            way_features['ways'].append({
                'way_id'     : way.id,
                'name'       : way.tags.get('name', 'unknown'),
                'coordinates': coordinates,
            })

        # Construct a polygon from all the projected coordinates and compute its area in square kilometers
        polygon_projected = Polygon(all_coordinates_projected)
        total_area = polygon_projected.area / 10**6

        # Add the total count of processed ways and the total area of all ways to the result
        way_features['way_count'] = len(way_features['ways'])
        way_features['total_area'] = total_area

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
    
