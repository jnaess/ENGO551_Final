import re
import os
import io

import numpy as np

import pandas as pd
from shapely.geometry import Point
import pkg_resources
from geopandas import GeoDataFrame
import json

import psycopg2
from sqlalchemy import create_engine
import shapely.geometry as sg
import shapely.ops as so
import matplotlib.pyplot as plt
import json
    
import time

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
import requests

from databaseManager import DatabaseManager

app = Flask(__name__)

#api URL
book_api = "https://www.googleapis.com/books/v1/volumes"

#Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = DatabaseManager()


@app.route('/')
def index():
    print("hi")
    
    return redirect("/live_feed")

@app.route('/field_management', methods=["GET","POST"])
def field_management():

    return render_template("field_management.html", 
                           json_string = db.load_fields())

@app.route('/process_field/<string:crop_type>/<string:poly>', methods=['POST'])
def process_field(crop_type, poly):
    #adds a new field
    db.new_field(crop_type=crop_type, geometry=poly) 
    
    return redirect('/field_management')
    
    
@app.route('/asset_management', methods=["GET","POST"])
def asset_management():       
    #the main asset management page
    
    #load all current assets
    assets = db.select_all("assets")
    
    return render_template("asset_management.html", assets = assets)

@app.route('/new_asset', methods=["GET", "POST"])
def new_asset():
    if request.method == "POST":
        #then it was sent in correctly
        
        #before asigning session variables
        asset_class = request.form.get("class")
        asset_name = request.form.get("name")
        
        #add new asset to database
        db.new_asset(asset_class, asset_name)
        
    return redirect('/asset_management')

@app.route('/live_feed')
def live_feed():
    return render_template("live_feed.html", 
                           json_string = db.load_fields())

@app.route('/asset_tracker')
def asset_tracker():
    return render_template("asset_tracker.html")


@app.route('/process_asset/<string:asset_name>/<string:asset_class>/<asset_id>/<string:lat>/<string:long>', methods=['POST'])
def process_asset(asset_name, asset_id, asset_class, lat, long):
        
    db.new_asset_location(asset_id, lat, long)
        
    return redirect('/asset_tracker')

@app.route('/api/assets_locations', methods = ['GET'])
def api_asset_locations():
    #http://127.0.0.1:5000/api/assets_locations?start=2022-04-23%2000:00:00&end=2022-04-26%2000:00:00&field_type=beans&key=password
    start = ''
    end = ''
    key = ''
    asset_id = 0
    field_id = 0
    field_type = 'wheat'
    data = False
    
    if 'key' in request.args:
        key = request.args['key']
        if key == 'password':
            #then api key is valid
            if 'start' in request.args:
                #DD/MM/YYYY HH:MM:SS
                start = request.args['start']
                

                if 'end' in request.args:
                    #DD/MM/YYYY HH:MM:SS
                    end = request.args['end']
                else:
                    #then start and end date are the same
                    end = start

            if 'asset_id' in request.args:
                #is not used
                asset_id = int(request.args['asset_id'])
                
            if 'field_id' in request.args:
                #int
                field_id = int(request.args['field_id'])
                
            if 'field_type' in request.args:
                field_type = request.args['field_type']
            
            print(start)
            print(end)
            print(field_id)
            
            data = db.get_assets_within_fields(start = start, 
                                               end = end, 
                                               field_type = field_type)
            
            return data.to_json()
    
        return "Invalid API Key"

    
    #find which fields that an asset has been in over a given period of time
        ##check that dates are working
        ##check that moment in time is working
        
    #return as a json
    
    return "Hello World"

@app.route('/api/test', methods = ['GET'])
def api_test():
    stuff = db.get_assets_within_fields()

    return stuff.to_json()