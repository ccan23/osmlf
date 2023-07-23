#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as et

from .overpass_calculations import calculations

class operations:

    def filter_nodes(nodes: list, key: str, value: str) -> list:
        """
        Filters a list of OSM nodes based on a specified key-value pair.

        Args:
            nodes (list): A list of OSM node objects.
            key (str): The key to filter on.
            value (str): The value to match for the specified key.

        Returns:
            list: A filtered list of OSM nodes that match the specified key-value pair.
        """

        # Using list comprehension to find nodes with the specified key and value in all ways and return it
        return [node for node in nodes if key in node.tags and node.tags[key] == value]

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
    
    def subareas(osm_id):
        # Response
        response = requests.get(f'https://www.openstreetmap.org/api/0.6/relation/{osm_id}/full')

        # Remove the first line which is not part of the XML data
        content_fixed = '\n'.join(response.text.split('\n')[1:])

        # Parse the XML content
        root = et.fromstring(content_fixed)

        # Initialize a set to store the ids of all subareas
        all_subarea_ids = set()

        # Initialize a variable to store the id of the top-level area
        top_level_area_id = None

        # Initialize an empty dictionary to store the counts
        subareas_count = {}

        # Iterate over the relations in the root
        for relation in root.findall('relation'):
            # Initialize a count for this relation
            count = 0
            # Iterate over the children of the relation
            for child in relation:
                # If the child is a 'member' with role 'subarea', increment the count
                if child.tag == 'member' and child.get('role') == 'subarea':
                    count += 1
                    # Add the ref of the child to the set of all subarea ids
                    all_subarea_ids.add(child.get('ref'))
            # If the relation has a 'name' tag, add the count to the dictionary
            name_tag = relation.find("tag[@k='name']")
            if name_tag is not None:
                subareas_count[name_tag.get('v')] = count
                # If this relation's id is not in the set of all subarea ids, it's the top-level area
                if relation.get('id') not in all_subarea_ids:
                    top_level_area_id = relation.get('id')

        # Remove the top-level area from the dictionary
        if top_level_area_id is not None:
            top_level_name = root.find(f"relation[@id='{top_level_area_id}']/tag[@k='name']").get('v')
            subareas_count.pop(top_level_name, None)

        return subareas_count
    
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
