# Surf's Up an sql-alchemy-challenge

Climate analysis of Hawaii using sqlalchemy to access sqlite and Matplotlib and Pandas and setting up JSON responses via flask 

### Step 1 - Climate Analysis and Exploration - SQLAlchemy ORM queries, Pandas, and Matplotlib - (Hawaii_climate_analysis.ipynb)

To begin set-up the dependancies required for the task at hand. These are standard libraries used in data analysis:

##### matplotlib libraries 

    %matplotlib inline
    from matplotlib import style
    style.use('fivethirtyeight')
    import matplotlib.pyplot as plt

##### Next were numpy, pandas and date time

    import numpy as np
    import pandas as pd
    import datetime as dt
  
##### Reflect Tables into SQLAlchemy ORM

** Python SQL toolkit and Object Relational Mapper **
  
    import sqlalchemy
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine, func, inspect, desc
    
##### Now to set up for a series of queries using session objects
    
**set up engine for sqlite database stored in the Resources folder**
        
        engine = create_engine("sqlite:///Resources/hawaii.sqlite",echo=False)
        
        
        
        
**Reflect an existing database into a new model**
        
        Base = automap_base()
        
**Reflect the tables**
       
       Base.prepare(engine, reflect=True) 
        
**Save references to each table in the sqlite DB that we want to access**
        
        Meas = Base.classes.measurement
        Sta = Base.classes.station
        
##### After the set-up is created session queries were run 

-**Precipitation**
- Precipitation data for the 12 month period ending 2017-8-23
- Dates and rainfall amounts selected
- The values were sorted by date in a Pandas dataframe
- A plot was created using Matplotlib
- Pandas was used to generate summary statistics

![Hawaii Rainfall 2016-2017 season ](https://github.com/SJLimburg/sql-alchemy-challenge/blob/main/Rain%20in%20Hawaii%202016-2017%20season%20-%20homework.png)

-**Weather Stations**
- Calculated the total number of stations
- List the stations and observation counts in descending order (tobs)
- Select the most active station in terms of observations made (Waikiki was the result)
- Retrieve the last 12 months of temperature observation data from the most active site
- Plot the results as a histogram with bins=12

![Waikiki Weather Station Temperature Observations](https://github.com/SJLimburg/sql-alchemy-challenge/blob/main/Waikiki%20Weather%20Station%20Temperature%20Observations.png)

### Step 2 - Climate App - Sdesign a Flask API based on the queries just developed (app.py)

**Import flask and jsonify libraries**

        from flask import Flask, jsonify

**Set-up Flask to create the APIs for the climate app**

        app = Flask(__name__)
 
 **Setup routes as defined in instructions and return Jsonified data to the user**
 
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

##### Complete code can be found in app.py files

# Bonus data can be found in the Jupyter Notebook as well

