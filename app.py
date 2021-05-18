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

# Setup Flask app
app = Flask(__name__)

# Setup routes
@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii Climate API<br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    last_year_prcp = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).order_by(Measurement.date.desc()).all()
    
    # dict reference - https://medium.com/analytics-vidhya/python-dictionary-and-json-a-comprehensive-guide-ceed58a3e2ed
    precip = {date: prcp for date, prcp in last_year_prcp}
    return jsonify(precip)

if __name__ == '__main__':
    app.run(debug=True)
