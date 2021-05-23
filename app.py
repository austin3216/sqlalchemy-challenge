# Import depedencies
import numpy as np
import pandas as pd
import datetime as dt

# Import Python SQL Toolkit
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Import flask, jsonify
from flask import Flask, jsonify 

# Database connection
engine = create_engine("sqlite:///sqlalchemy-challenge/Resources/hawaii.sqlite")

# Reflect database and tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# print(Base.classes.keys())

# Save references as variables
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session
session = Session(engine)

# Setup Flask app
app = Flask(__name__)

# Setup routes

# welcome route listing all available routes

@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii Climate API<br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start</br>"
        f"/api/v1.0/temp/start/end"
    )

# precipitation route

@app.route("/api/v1.0/precipitation")
def precipitation():

    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).order_by(Measurement.date.desc()).all()
    
    # dict reference - https://medium.com/analytics-vidhya/python-dictionary-and-json-a-comprehensive-guide-ceed58a3e2ed
    precip = {date: prcp for date, prcp in last_year_prcp}
    return jsonify(precip)

# stations route

@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    stations_all = list(np.ravel(results))
    
    return jsonify(stations_all)

@app.route("/api/v1.0/tobs")
def tobs():

    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the primary station for all tobs from the last year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= one_year_ago).all()

    # Convert list of tuples into normal list
    temps = list(np.ravel(results))

    return jsonify(temps)

# start and start/end routes

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def measures(start=None, end=None):

    # define select statement for min, avg, max
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        # calculate min, avg, max for dates greater than start
        results = session.query(*sel).filter(Measurement.date >= start).all()
        
        # Unravel results 
        stats = list(np.ravel(results))
        return jsonify(stats)

    else:

        # calculate min, avg, max betwee start and stop dates
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        
        # Unravel results
        stats = list(np.ravel(results))
        return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)