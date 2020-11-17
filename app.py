import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup using sqlalchemy
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table 
Meas = Base.classes.measurement
Sta = Base.classes.station

#############################
# Set-up Flask
#############################
app = Flask(__name__)

#############################
# Set-up Routes 
#############################
@app.route("/")
def welcome():
    """List all Available API routes - these routes were defined in the instructions"""
    return (
        f"Plan your trip to  Hawaii using this Climate Analysis API!<br/>\
        Note: To look at temps please specify start and end date as yyyy-mm-dd<br/>\
        Dates must be between 2010-01-01 and 2017-08-23<br/>\
        Query returns Min, Avg, Max  <br/>\
            <br/>"
        f"Available Pages:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end"
    )


# set-up APIs for the first route - precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database; we did this in Jupyter notebook previously
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #Create session link from Python to DB
    session = Session(engine)
    # Convert the query results to a dictionary using date as the key and prcp as the value
    results_rain = session.query(Meas.date, Meas.prcp).\
        filter(Meas.date >= prev_year).all()
    # close session
    session.close()   
    # Create the dict from the rainfall query date as the key and prcp as the value
    rain = {date: prcp for date, prcp in results_rain}
    # Return the JSON representation of your dictionary
    return jsonify(rain)
    
# set-up APIs for the stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset"""
    #Create session link from Python to DB
    session = Session(engine)
    #Create query for all stations
    results_stations = session.query(Sta.station).all()
    # close session
    session.close() 
    # use numpy unravel to convert to a list
    stations = list(np.ravel(results_stations))
    return jsonify(stations=stations)

# set-up APIs for the temperature observations
@app.route("/api/v1.0/tobs")
def temp_monthly():
    """Return the temperature observations (tobs) for previous year."""
    # Calculate the date 1 year ago from last date in database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #Create session link from Python to DB
    session = Session(engine)   
    # Query the primary station for all tobs from the last year
    results = session.query(Meas.tobs).\
        filter(Meas.station == 'USC00519281').\
        filter(Meas.date >= prev_year).all()
    # close session
    session.close()     
   # use numpy unravel to convert to a list
    temps = list(np.ravel(results))

    # Return the results
    return jsonify(temps=temps)

# set-up APIs for the temperature Min; Avg & Max over a date range
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""  
    # Select statement
    calcs = [func.min(Meas.tobs), func.avg(Meas.tobs), func.max(Meas.tobs)]
    #Create session link from Python to DB
    session = Session(engine)  
    if not end:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        results_temp = session.query(*calcs).\
            filter(Meas.date >= start).all()
        session.close()
        # use numpy unravel to convert to a list
        temps = list(np.ravel(results_temp))
        return jsonify(temps=temps)

    # calculate TMIN, TAVG, TMAX with start and end
    results_temp = session.query(*calcs).\
        filter(Meas.date >= start).\
        filter(Meas.date <= end).all()
    session.close()
    # use numpy unravel to convert to a list
    temps = list(np.ravel(results_temp))
    return jsonify(temps=temps)

if __name__ == '__main__':
    app.run()