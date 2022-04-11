import pandas as pd
import shapely.geometry as sg
from geopandas import GeoDataFrame
import json

class Assistant():
    """
    Contains assistance functions for the app
    """
    
    def __init__(self):
        """
        """
        return
        
    def load_fields(self):
        """
        loads all fields
        """
        df = self.fields_all()

        geo = []
        for j in range(df.index[-1]+1):
            test2 = df.geometry[j]
            res = test2.replace('(','').replace(')','').split(',')

            coords = []
            for i in range(0,len(res),2):
                coords.append((float(res[i+1]),float(res[i])))
            final = tuple(coords)

            geo.append(sg.Polygon(final))
        df["geometry"] = geo

        gdf = GeoDataFrame(df, geometry='geometry')

        geoJSON = gdf.to_json()
        geoJSON = json.loads(geoJSON)
        
        return geoJSON