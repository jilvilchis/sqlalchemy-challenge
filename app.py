import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#Data base setup
engine = create_engine("sqlite:///titanic.sqlite")
#Establishing the base
Base = automap_base()
Base.prepare(engine, reflect=True)
Passenger = Base.classes.passenger

# Flask setup
app = Flask(__name__)

#Routes
@app.route("/")
def home():
    return f"""
        <p>Available routes:</p>
        <p>/api/names</p>
        <p>/api/passengers</p>
    """

@app.route("/api/names")
def names():
    session = Session(engine)
    results = session.query(Passenger.name).all()
    results = list(np.ravel(results))
    session.close()
    return jsonify(results)

@app.route("/api/passengers")
def passengers():
    session = Session(engine)
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()
    session.close()
    
    all_passengers = []
    for name, age, sex in results:
        all_passengers.append({
            "name":name,
            "age": age,
            "sex": sex
        })

    return jsonify(all_passengers)

if __name__ == "__main__":
    app.run(debug=True)