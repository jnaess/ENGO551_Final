
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
    
    print(assets)
    print(assets.iterrows())
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


@app.route('/process_asset/<string:asset_name>/<string:asset_class>/<string:asset_id>/<string:lat>/<string:long>', methods=['POST'])
def process_asset(asset_name, asset_id, asset_class, lat, long):
    
    #adds a new asset location   
    asset_name = request.form.get("asset_name_id")
    asset_id = request.form.get("asset_id_id")
    asset_class = request.form.get("asset_class_id")
    lat = request.form.get("lat_id")
    long = request.form.get("long_id")
        
    db.new_asset_location(asset_id, lat, long)
        
    return redirect('/asset_tracker')