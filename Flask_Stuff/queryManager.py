import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import json


class QueryManager():
    """
    """
    
    def __init__(self):
        """
        Desc:
        Input:
        Output:
        """
        
    
    def select_all(self, table = '"postgis"."simulations"'):
        """
        Desc:
            selects all rows from a column
        Input:
        Output:
        """
        return pd.read_sql_query(f'''SELECT * FROM {table} ''', self.engine)
    
    def fields_all(self, table = '"postgis"."fields"'):
        """
        Desc:
            querry to reteive all rows from the simulations table
        Input:
            con, connection to database
            table, table name to retrieve from
        Output:
        """
        return pd.read_sql_query(f'''SELECT * 
                        FROM {table} ''', self.engine)
    
    def new_field(self, crop_type, geometry, table = '"postgis"."fields"'):
        """
        Desc:
            inserts a new field with a given crop type
        Input:
        Output
        """
        crop_type=json.loads(crop_type)
    
        poly = json.loads(geometry)[0]


        coords = []

        for point in poly:
            coords.append((point[1],point[0]))

        poly_formatted = str(tuple(coords))

        #r1 = sg.Polygon(coords)
        print(poly_formatted)
        self.engine.execute(f"INSERT INTO {table}\
                       (farm_id, crop_type, geometry) VALUES ('{self.farm_id}', '{crop_type}', '{poly_formatted}')")
        
    def new_asset(self, asset_class, asset_name, table = '"postgis.""assets"'):
        """
        Desc:
            Inserts a new field with a given crop type
        Input:
        Output:
        """    
        self.engine.execute(f"INSERT INTO {table}\
                       (farm_id, name, class) VALUES ('{self.farm_id}', '{asset_name}', '{asset_class}')")
        
    def new_asset_location(self, asset_id, lat, long, table = '"postgis"."asset_locations"'):
        """
        Desc:
            Inserts a new asset location for searching
        Input:
        Output:
        """    

        #geog_type =f'({long} {lat})'
        #geog_type = "'POINT(%s %s)'" % (long, lat)


        #self.engine.execute(f"INSERT INTO {table}\
                       #(asset_id, location) VALUES ({asset_id}, {geog_type})")
        self.engine.execute(f"INSERT INTO {table}\
                       (asset_id, long, lat) VALUES (({5}), {long}, {lat})")
        
    def get_assets_within_fields(self):
        """
        Desc:
            returns id's of assets within any field
        Input:
        Output:
        """    
        return self.engine.execute("SELECT postgis.a_locations.id, postgis.fields.field_id\
                                FROM postgis.a_locations, postgis.fields\
                                WHERE ST_Contains(postgis.fields.geompoly, postgis.a_locations.geompt);")