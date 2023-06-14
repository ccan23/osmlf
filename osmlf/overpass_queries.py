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
    
    def generate_osm_query(osm_id: int, key: str) -> str:
        """
        Given an OpenStreetMap ID, a key, and a value, generate an Overpass QL query that retrieves 
        related way and relation objects from the OpenStreetMap database.
        
        Args:
            osm_id (int): The OpenStreetMap ID to base the query on.
            key (str): The key to use in the Overpass QL query.
            value (str): The value to match with the key in the Overpass QL query.

        Returns:
            str: A string that represents an Overpass QL query.
        """
        return f"""
        [out:json];
        rel({osm_id});
        map_to_area->.a;
        (
        way(area.a)["{key}"];
        relation(area.a)["{key}"];
        );
        out body;
        >;
        out geom qt;
        """
    