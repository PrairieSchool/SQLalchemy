# Flask section of homework

# Import dependencies

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from datetime import datetime, date
import numpy as np

from flask import Flask, jsonify

# Connect to database file and create Base, Engine, Session, etc
surf_engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = surf_engine.connect()
surf_base = automap_base()
surf_base.prepare(surf_engine, reflect=True)
surf_base.classes.keys()

Measurement = surf_base.classes.measurement
Station = surf_base.classes.station
Surf_ORM_Session = Session(surf_engine)


# Queries to be used on endpoints below

stations = Surf_ORM_Session.query(Station.station, Station.name).all()
precip_date = Surf_ORM_Session.query(Measurement.date, Measurement.prcp).all()

start_date = '2016-08-24'
end_date = '2017-08-23'
start_date_input = "2016-08-24"
end_date_input = '2017-08-23'


start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
start_date_input = datetime.strptime(start_date_input,"%Y-%m-%d").date()
end_date_input = datetime.strptime(end_date_input, "%Y-%m-%d").date()


tobs = Surf_ORM_Session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= start_date, Measurement.date <= end_date).\
    order_by(Measurement.date).all()


    
app = Flask(__name__)

# Home page: List all routes that are available.
@app.route("/")
def surf():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/Date_Precip<br/>"
        f"/api/v1.0/Stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start_date_input><br/>"
        f"/api/v1.0/start/end"
        
        
    )


# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary
@app.route("/api/v1.0/Date_Precip")
def precip():

    # Convert list of tuples into normal list
    xx = list(np.ravel(precip_date))

    return jsonify(precip_date)


# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/Stations")
def stations_names():

    # Convert list of tuples into normal list
    yy = list(np.ravel(stations))

    return jsonify(stations)

# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs_year():


    return jsonify(tobs)

@app.route("/api/v1.0/start/<start_date_input>")
def start(start_date_input):
       
    
    start_q = Surf_ORM_Session.query(Measurement.station, Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= start_date_input, Measurement.date <= end_date).\
            order_by(Measurement.date).all()    
            
    
    return jsonify(start_q)


@app.route("/api/v1.0/start/end")
def start_end():
    
    start_end_q = Surf_ORM_Session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= start_date_input, Measurement.date <= end_date_input).\
        order_by(Measurement.date).all()
    
    return jsonify(start_end_q)    


if __name__ == '__main__':
    app.run(debug=True)