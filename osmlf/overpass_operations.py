#!/usr/bin/env python3

from overpass_calculations import calculations

class operations:

    def filter_members(relations: list, role: str) -> list:
        """
        This function filters members of given relations based on the specified role.
        
        Args:
            relations (list): A list of OSM relation objects.
            role (str): The role to filter members by.

        Returns:
            list: A list of reference IDs for members with the specified role.
        """

        # Using list comprehension to find members with the specified role in all relations and return it
        return [member for relation in relations for member in relation.members if member.role == role]

    def filter_ways(ways: list, key: str, value: str) -> list:
        """
        Filter the list of OSM way objects based on a specific tag's key and value.
        
        Args:
            ways (list): A list of OSM way objects to filter.
            key (str): The key of the tag to check in each way.
            value (str): The value of the tag to match in each way.

        Returns:
            list: A new list of OSM way objects that have the specified tag key and value.

        Notes:
            Only way objects that contain the specified key in their tags and where the corresponding 
            value matches the specified value are included in the returned list. Way objects without 
            the specified key or with a different value for this key are excluded.
        """

        # Using list comprehension to find ways with the specified key and value in all ways and return it
        return [way for way in ways if key in way.tags and way.tags[key] == value]

    def select_utm_zone(lat: float, lon: float) -> str:
        """Select a UTM zone based on a location.

        Args:
            lat (float): latitude
            lon (float): longitude

        Returns:
            str: UTM projection string
        """
        
        # Calculate the UTM zone number
        zone_number = int((lon + 180) / 6) + 1

        # Determine the UTM hemisphere (north or south)
        hemisphere = 'north' if lat >= 0 else 'south'

        # Create the UTM projection string and return it
        return f'+proj=utm +zone={zone_number} +{hemisphere} +ellps=WGS84 +datum=WGS84 +units=m +no_defs'
    
    def subareas(relations: list) -> dict:
        """
        Function to identify subareas from a list of relation objects. 
        Each relation object is expected to have 'members' as one of its attributes. 
        Each member should have 'role' and 'ref' as attributes.
        
        Args:
            relations: A list of relation objects

        Returns:
            dict: A dictionary with total count of subareas and sorted list of subarea relation IDs.
        """

        # Get all subareas from given relations list
        subareas = operations.filter_members(relations=relations, role='subarea')

        # Return a dictionary with the total number of subareas and a sorted list of the reference IDs of the subareas
        return {
            'total_subareas'      : len(subareas), 
            'subarea_relation_ids': sorted([relation.ref for relation in subareas])
        }
    
    def total_area(relations: list, utm_zone: str) -> float:
        """
        Function to calculate the total area of a list of relations.
        Each relation object should have 'members', and each member should have 'geometry'.
        Each geometry should have 'lon' and 'lat' attributes.

        The function projects the geographical coordinates into a specified UTM zone
        before calculating the area for more accuracy.

        Args:
            relations: A list of relation objects.
            utm_zone : UTM zone

        Returns:
            dict: A dictionary that contains way features, count of ways, and total area.
        """

        # Get all outers from given relation list
        outers = operations.filter_members(relations=relations, role='outer')

        # # Get all areas from outers
        return calculations.area_of_members(members=outers, utm_zone=utm_zone)
