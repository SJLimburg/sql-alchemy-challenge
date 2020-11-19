# Surf's Up an sql-alchemy-challenge

Climate analysis of Hawaii using sqlalchemy to access sqlite and Matplotlib and Pandas and setting up JSON responses via flask 

### Step 1 - Climate Analysis and Exploration - SQLAlchemy ORM queries, Pandas, and Matplotlib - (Hawaii_climate_analysis.ipynb)

Some items were given to set-up the dependancies required for the task at hand:

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
