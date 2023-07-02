class queries:

    def administrative(osm_id: int) -> str:
        """Given osm_id's relation object
        
        Returns:
            str: Query that gives osm id's relation object
        """
        return f"""
        [out:json];
        rel({osm_id});
        (._;>;);
        out geom;
        """
    
    def generate_osm_query(osm_id: int, key: str, values: list) -> str:
        """
        Given an OpenStreetMap ID, a key, and a list of values, generate an Overpass QL query that retrieves 
        related node, way and relation objects from the OpenStreetMap database for any of the given values.
        
        Args:
            osm_id (int): The OpenStreetMap ID to base the query on.
            key (str): The key to use in the Overpass QL query.
            values (list): The values to match with the key in the Overpass QL query (Optional).

        Returns:
            str: A string that represents an Overpass QL query.
        """

        # Create the string representing the list of possible key-value matches
        if values:
            value_string = ''.join([f'node(area.a)["{key}"="{value}"];way(area.a)["{key}"="{value}"];relation(area.a)["{key}"="{value}"];' for value in values])
            
        else:
            value_string = f'node(area.a)["{key}"];way(area.a)["{key}"];relation(area.a)["{key}"];'

        # Insert the value string into the Overpass QL query
        return f"""
        [out:json];
        rel({osm_id});
        map_to_area->.a;
        (
        {value_string}
        );
        out body;
        >;
        out geom qt;
        """
    