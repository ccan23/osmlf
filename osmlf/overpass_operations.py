#!/usr/bin/env python3

from overpass_calculations import calculations

class operations:

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
        subareas = calculations.filter_members(relations=relations, role='subarea')

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
        outers = calculations.filter_members(relations=relations, role='outer')

        # # Get all areas from outers
        return calculations.area_of_members(members=outers, utm_zone=utm_zone)
