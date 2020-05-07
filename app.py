import pandas as pd
import numpy as np
import datetime as dt
import os
import sqlalchemy
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, MetaData, inspect, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite", echo=False)

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(bind=engine)

app = Flask(__name__)

# Home page.
#List all routes that are available.

@app.route("/")
def home():
    routes = (f"welcome to the hawaii climate analysis API <br/>"
    f"routes <br/>"
    f"/api/v1.0/precipitation <br/>"
    f"/api/v1.0/stations <br/>"
    f"/api/v1.0/tobs <br/>"
    f"/api/v1.0/start <br/>"
    f"/api/v1.0/start/end <br/>")

    return routes

# Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitationofday():
    lastyear = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=lastyear).all()
    precipitation = {date: prcp for date, prcp in results}
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    lastyear = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date>=lastyear).all()
    temperatures = list(np.ravel(results))
    return jsonify(temperatures)

@app.route("/api/v1.0/<start>")
def starter(start):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    temperatures = list(np.ravel(results))
    return jsonify(temperatures)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temperatures = list(np.ravel(results))
    return jsonify(temperatures)

if __name__ == '__main__':
    app.run(debug=True)