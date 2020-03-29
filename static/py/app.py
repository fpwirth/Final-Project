# Docs on session basics

import numpy as np
import pandas as pd
import os


from flask import Flask, jsonify



#################################################
# Database Setup
#################################################

# variables to populate the database connection string
# db_user = 'postgres'
# db_password = 'postgres'
# db_host = 'localhost'
# db_port = 5432

# This database must already exist
# db_name = "city_state_data_db"

# engine = create_engine(f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
# Base.metadata.create_all(engine)

# reflect an existing database into a new model
# Base = automap_base()
# Base.prepare(engine, reflect=True)

# Save reference to the table
weatherData = pd.read_csv("../data/selected_weather_data_for_visual.csv")

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/weather/date/<date_filter><br/>"
        f"/api/v1.0/weather/dateRange/<dateStart>/<dateEnd><br/>"
    )


@app.route("/api/v1.0/weather/date/<date_filter>")
def stateData(date_filter):
    """Return a list of all weather for the state"""

    # Query all passengers
    weather_sel = weather_data('date_field' == date_filter)

    # close the session to end the communication with the database
    # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))
    all_data = []
    # for weather, index in weather_sel:
    for index, weather in weather_sel.iterrows():
        weather_dict = {}
        weather_dict["date"] = weather['date_field']
        weather_dict["tempMax"] = weather['tempMax']
        weather_dict["tempMin"] = weather['tempMin']
        weather_dict["tempAvg"] = weather['tempAvg']
        weather_dict["precipitation"] = weather['precipitation']
        all_data.append(weather_dict)

    return jsonify(all_data)


@app.route("/api/v1.0/weather/dateRange/<date_start>/<date_end>")
def all_states(date_start, date_end):
    """Return a list of all weather for the state"""

    # Query all passengers
    weather_sel = weather_data('date_field' == date_filter)

    # close the session to end the communication with the database
    # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))
    all_data = []
    # for weather, index in weather_sel:
    for index, weather in weather_sel.iterrows():
        weather_dict = {}
        weather_dict["date"] = weather['date_field']
        weather_dict["tempMax"] = weather['tempMax']
        weather_dict["tempMin"] = weather['tempMin']
        weather_dict["tempAvg"] = weather['tempAvg']
        weather_dict["precipitation"] = weather['precipitation']
        all_data.append(weather_dict)

    return jsonify(all_data)


#     return jsonify(all_names)


# @app.route("/api/v1.0/passengers")
# def passengers():
#     """Return a list of passenger data including the name, age, and sex of each passenger"""

#     # Open a communication session with the database
#     session = Session(engine)

#     # Query all passengers
#     results = session.query(Passenger).all()

#     # close the session to end the communication with the database
#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for passenger in results:
#         passenger_dict = {}
#         passenger_dict["name"] = passenger.name
#         passenger_dict["age"] = passenger.age
#         passenger_dict["sex"] = passenger.sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
