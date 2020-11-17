import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Meas = Base.classes.measurement
Sta = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#############################
# Set-up Flask
#############################
app = Flask(__name__)

#############################
# Set-up Routes 
#############################
@app.route("/")
def home():
    return (
        f"Plan your trip to  Hawaii using this Climate Analysis API!<br/>"
        f"Available Pages:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

# set-up APIs for the first route - precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database - we did this in Jupyter notebook previously
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    # Create the Query for the date and prcp for the last year
    rainfall = session.query(Meas.date, Meas.prcp).\
        filter(Meas.date >= prev_year).all()
    
    # Return the JSON representation of your dictionary
    # Create the dict from the rainfall query date as the key and prcp as the value
    precip = {date: prcp for date, prcp in rainfall}
    # Jsonify the Dictionary
    return jsonify(precip)
    
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    stationdata = session.query(Sta.station).all()

    # Unravel results into a 1D array and convert to a list
    stations = list(np.ravel(stationdata))
    return jsonify(stations=stations)
    print(stations)


