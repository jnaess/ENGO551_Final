
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
#db = SQL("postgres://tdordoxeldwmqu:8f5dd3c7322b6a83fa9279eb76cdc139979adcc7b3c03ace597bac1661d1e696@ec2-34-239-196-254.compute-1.amazonaws.com:5432/dal40v64r9dbnv")


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/asset_management', methods=["GET","POST"])
def asset_management():
    return render_template("asset_management.html")

@app.route('/process_field/<string:crop_type>/<string:poly>', methods=['POST'])
def process_field(crop_type, poly):
    #adds a new field
    db.new_field(crop_type=crop_type, geometry=poly) 
    
    return('/asset_management')
    
    
@app.route('/field_management')
def field_management():
    return render_template("field_management.html")

@app.route('/live_feed')
def live_feed():
    return render_template("live_feed.html")

@app.route('/tester')
def tester():
    return render_template("tester.html")