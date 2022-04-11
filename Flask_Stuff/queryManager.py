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
        
    
    def select_all(self, table = "simulations"):
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
    
    def new_field(self, crop_type, geometry, table = "fields"):
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
    
        self.engine.execute(f"INSERT INTO {table}\
                       (farm_id, crop_type, geometry) VALUES ('{self.farm_id}', '{crop_type}', '{poly_formatted}')")