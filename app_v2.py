import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Data base setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#Establishing the base
Base = automap_base()
Base.prepare(engine, reflect=True)
Station = Base.classes.station
Measurement = Base.classes.measurement

# Flask setup
app = Flask(__name__)

#Routes
@app.route("/")
def home():
    return f"""
        <p>Available routes:</p>
        <p>/api/v1.0/precipitation</p>
        <p>/api/v1.0/stations</p>
        <p>/api/v1.0/tobs</p>
        <p>/api/v1.0/temp_(Start)/<start></p>
        <p>/api/v1.0/temp_(Start/End)/<start>/<end></p>
    """

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date>'2016-08-22', Measurement.prcp!=0)
    session.close()
#Using Dictionary comprehensions to get Date as key and prcp as values
    precipitation={date:prcp for date, prcp in results}
    return jsonify(precipitation)    

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    station_ls = list(np.ravel(results))
    return jsonify(station_ls)
    
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs)\
            .filter(Measurement.date>'2016-08-22', Measurement.tobs!=0)\
            .filter(Measurement.station=='USC00519281')
    session.close()
    ltm_tobs = []
    for date, tobs in results:
        ltm_tobs.append({
            "date":date,
            "tobs": tobs,
        })
    return jsonify(ltm_tobs)    

@app.route("/api/v1.0/temp_(Start)/<start>")
def temp(start=None):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date>start).all()
    session.close()
    temperature = list(np.ravel(results))
    return jsonify({'Start_Date':start, 'Min_Max_Avg': temperature})


@app.route("/api/v1.0/temp_(Start/End)/<start>/<end>")
def temp2(start=None, end=None):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date.between(start,end)).all()
    session.close()
    temperature = list(np.ravel(results))
    return jsonify({'Start_Date':start, 'End_Date':end, 'Min_Max_Avg': temperature})

if __name__ == "__main__":
    app.run(debug=True)