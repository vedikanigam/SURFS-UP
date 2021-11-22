import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
engine = create_engine('sqlite:///hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

app = Flask(__name__)
@app.route('/')
def welcome():
    return (
    '''
    <h1>Welcome to the Climate Analysis API!</h1>
    <h5>Available Routes:</h5>
    <ul><li>/api/v1.0/precipitation</li>
    <li>/api/v1.0/stations</li>
    <li>/api/v1.0/tobs</li>
    <li>/api/v1.0/temp/start/end</li></ul>
    ''')

@app.route('/api/v1.0/precipitation')
def precipitation():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    return { date:prcp for date,prcp in session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >=prev_year).all() }

@app.route('/api/v1.0/stations')
def stations():
    return { station:name for station,name in session.query(Station.station,Station.name).all() }

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify (temps=temps)

@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def stats(start, end='2017-08-23'):
    sel=[func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)]

    results =  session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temps = list(np.ravel(results))
    return jsonify(temps)
    
if __name__ == '__main__':
    app.run(debug=True)


