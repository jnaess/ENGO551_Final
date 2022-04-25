import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import json
import time
import datetime


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
    
    def fields_all(self, table = "fields"):
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
        points_str = ""

        for point in poly:
            points_str += str(point[0]) + " " + str(point[1]) + ","
            coords.append((point[1],point[0]))
            
        poly_formatted = str(tuple(coords))
        points_str = points_str[:-1]
        print(points_str)

        #r1 = sg.Polygon(coords)
    
        self.engine.execute(f"INSERT INTO {table}\
                       (farm_id, crop_type, points, geometry) VALUES ('{self.farm_id}', '{crop_type}', '{points_str}', '{poly_formatted}')")
        self.engine.execute(f"UPDATE {table}\
                        SET geompoly = ST_Transform(ST_SetSRID(ST_MakePolygon(ST_GeomFromText('LINESTRING(' || points || ')')), 4269), 3776)")
        
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
        
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        print(int('asset_id'))

        #self.engine.execute(f"INSERT INTO {table}\
                       #(asset_id, location) VALUES ({asset_id}, {geog_type})")
        self.engine.execute(f"INSERT INTO {table}\
                       (asset_id, date,  long, lat) VALUES (( {int(7.6)} ), '{timestamp}', {long}, {lat})")
        self.engine.execute(f"UPDATE {table} SET geompt = ST_Transform(ST_SetSRID(ST_MakePoint(long, lat), 4269), 3776)")
        
        
    def get_assets_within_fields(self, start = '2022-04-23 00:00:00', 
                                 end = '2022-04-26 00:00:00',
                                 field_id = 2,
                                field_type = 'beans'):
        """
        Desc:
            returns id's of assets within any field
        Input:
        Output:
        """        
        return pd.read_sql_query(f"SELECT asset_locations.asset_id\
                                FROM asset_locations, fields\
                                WHERE crop_type = '{field_type}' \
                                        AND date BETWEEN '{start}'::timestamp AND '{end}'::timestamp \
                                        AND ST_Contains(fields.geompoly, asset_locations.geompt);", self.engine)