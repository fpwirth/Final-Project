# Docs on session basics

import numpy as np
import pandas as pd
import os
import sys
from collections import OrderedDict

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin


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
aggData = pd.read_csv("../data/agg_hist_311_data.csv")
censusData = pd.read_json("../data/census_data.json")
weatherData['date_field_str'] = weatherData['date_field_str'].astype('str')
weatherData['yr'] = weatherData['yr'].astype('str')
censusData['zipcode'] = censusData['Zipcode'].astype('str')
aggData['zipcode'] = aggData['zipcode'].astype('str')
aggData['yr'] = aggData['yr'].astype('str')
aggData['date_field_str'] = aggData['date_field_str'].astype('str')
# aggData['date_field'] = aggData['date_field'].dt.date

# month = dict(one='January',
#                  two='February',
#                  three='March',
#                  four='April',
#                  five='May',
#                  six='June',
#                  seven='July',
#                  eight='August',
#                  nine='September',
#                  ten='October',
#                  eleven='November',
#                  twelve='December'
#                  )
# monthShort = dict(one='Jan',
#                  two='Feb',
#                  three='Mar',
#                  four='Apr',
#                  five='May',
#                  six='Jun',
#                  seven='Jul',
#                  eight='Aug',
#                  nine='Sep',
#                  ten='Oct',
#                  eleven='Nov',
#                  twelve='Dec'
#                  )

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
monthsDict = {'Jan': 1,'Feb' : 2,'Mar': 3,'Apr': 4,'May': 5,'Jun': 6,'Jul': 7,'Aug': 8,'Sep': 9,'Oct': 10,'Nov': 11,'Dec': 12}


print(censusData.head(5), file=sys.stderr)
print(aggData.head(5), file=sys.stderr)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'



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
    weather_sel = weatherData[weatherData['date_field_str'] == str(date_filter).strip()]
    print('data in filter:'+ str(date_filter), file=sys.stderr)
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
    weather_sel = weatherData[weatherData['date_field_str'] >= date_start]
    weather_sel = weather_sel[weather_sel['date_field_str'] <= date_end]

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

@app.route("/api/v1.0/census/zipcode/<zipcode_filter>")
def zipCodeData(zipcode_filter):
    """Return a list of all weather for the state"""

    # Query all passengers
    census_sel = censusData[censusData['zipcode'] == str(zipcode_filter).strip()]
    print('data in filter:'+ str(zipcode_filter), file=sys.stderr)
    # close the session to end the communication with the database
    # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))
    all_data = []
    # for weather, index in weather_sel:
    for index, census in census_sel.iterrows():
        census_dict = {}
        census_dict["zipcode"] = census['zipcode']
        census_dict["Population"] = census['Population']
        census_dict["MedianAge"] = census['Median Age']
        census_dict["HouseholdIncome"] = census['Household Income']
        census_dict["PerCapitaIncome"] = census['Per Capita Income']
        census_dict["PovertyRate"] = census['Poverty Rate']
        census_dict["TotalHouseholds"] = census['Total Households']
        census_dict["TotalOwnerOccupied"] = census['Total Owner Occupied']
        census_dict["PerOwnerOccupied"] = census['% Owner Occupied']

        all_data.append(census_dict)

    return jsonify(all_data)

@app.route("/api/v1.0/getAllZipCodes")
def getAllZipCodes():
    """Return a list of all weather for the state"""

    allZips = aggData.zipcode.unique();

    return jsonify(allZips.tolist())

@app.route("/api/v1.0/getAllTypes")
def getAllTypes():
    """Return a list of all weather for the state"""

    allServs = aggData.serv_type.unique();

    return jsonify(allServs.tolist())

@app.route("/api/v1.0/getAllDates")
def getAllDates():
    """Return a list of all weather for the state"""

    allDates = aggData.date_field_str.unique();

    return jsonify(allDates.tolist())


@app.route("/api/v1.0/getAllNeib")
def getAllNeib():
    """Return a list of all weather for the state"""

    allDates = aggData.neighborhood.unique();

    return jsonify(allDates.tolist())



@app.route("/api/v1.0/houston311/zipcode/date/type/<zipcode_filter>/<date_filter>/<type_filter>")
def houston311byAll(zipcode_filter, date_filter, type_filter):
    """Return a list of all weather for the state"""

    # Query all passengers
    agg_sel = aggData[aggData['zipcode'] == str(zipcode_filter).strip()]
    print('data in filter:'+ str(zipcode_filter), file=sys.stderr)
    agg_sel = agg_sel[agg_sel['date_field_str'] == str(date_filter).strip()]
    print('data in filter:'+ str(date_filter), file=sys.stderr)
    agg_sel = agg_sel[agg_sel['serv_type'] == str(type_filter).strip()]
    print('data in filter:'+ str(type_filter), file=sys.stderr)
    # close the session to end the communication with the database
    # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))
    all_data = []
    # for weather, index in weather_sel:
    for index, census in agg_sel.iterrows():
        census_dict = {}
        census_dict["zipcode"] = census['zipcode']
        census_dict["Population"] = census['Population']
        census_dict["MedianAge"] = census['Median Age']
        census_dict["HouseholdIncome"] = census['Household Income']
        census_dict["PerCapitaIncome"] = census['Per Capita Income']
        census_dict["PovertyRate"] = census['Poverty Rate']
        census_dict["TotalHouseholds"] = census['Total Households']
        census_dict["TotalOwnerOccupied"] = census['Total Owner Occupied']
        census_dict["PerOwnerOccupied"] = census['% Owner Occupied']

        all_data.append(census_dict)

    return jsonify(all_data)


@app.route("/api/v1.0/houston311/top10Types")
def houston311Top10():
    """Return a list of all weather for the state"""
    aggTypes = aggData.groupby(['serv_type']).agg(
    # Get max of the duration column for each group
    count_issues=('serv_type', 'count'))  
    aggTypes.reset_index(inplace=True)
    aggTypes.sort_values('count_issues',ascending=False,inplace=True)
    aggTypes = aggTypes.head(10)
    # close the session to end the communication with the database
    # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))
    all_data = []
    # for weather, index in weather_sel:
    for index, row in aggTypes.iterrows():
        data_dict = {}
        data_dict["serv_type"] = row.serv_type
        data_dict["count_issues"] = row.count_issues

        all_data.append(data_dict)

    return jsonify(all_data)




@app.route("/api/v1.0/houston311/ByMonth")
def houston311top10ByMonth():
    """Return a list of all weather for the state"""
    aggTypes = aggData.groupby(['date_month']).agg(
    # Get max of the duration column for each group
    count_issues=('serv_type', 'count')) 
    weathAgg = weatherData.groupby(['date_month']).agg(
    prec=('precipitation', 'sum'),
    avg_max=('tempMax', 'mean'))

    aggTypes.reset_index(inplace=True)
    weathAgg.reset_index(inplace=True)
 
    # close the session to end the communication with the database
    # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))
    all_data = []
    # for weather, index in weather_sel:
    for index, row in aggTypes.iterrows():
        data_dict = {}
        data_dict["date_month"] = row.date_month
        data_dict["count_issues"] = row.count_issues
        for index1, row1 in weathAgg.iterrows():
            if (row1.date_month == row.date_month):
                data_dict["prec"] = row1.prec
                data_dict["avg_max"] = row1.avg_max

        all_data.append(data_dict)

    return jsonify(all_data)


@app.route("/api/v1.0/houston311/top10Types/zip/<zip_filter>/year/<year_filter>/neib/<neib_filter>/type/<type_filter>")
def houston311Top10byZip(zip_filter, year_filter,neib_filter,  type_filter):
    """Return a list of all weather for the state"""
    agg_sel = aggData
    if (zip_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['zipcode'] == str(zip_filter).strip()]
    if (year_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['yr'] == str(year_filter).strip()]
    if (neib_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['neighborhood'] == str(neib_filter).strip()]
    if (type_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['serv_type'] == str(type_filter).strip()]
    print('data in filter:'+ str(zip_filter), file=sys.stderr)
    aggTypes = agg_sel.groupby(['serv_type']).agg(
    # Get max of the duration column for each group
    count_issues=('serv_type', 'count'))  
    aggTypes.reset_index(inplace=True)
    aggTypes.sort_values('count_issues',ascending=False,inplace=True)
    aggTypes = aggTypes.head(10)
    # close the session to end the communication with the database
    # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))
    all_data = []
    # for weather, index in weather_sel:
    for index, row in aggTypes.iterrows():
        data_dict = {}
        data_dict["serv_type"] = row.serv_type
        data_dict["count_issues"] = row.count_issues

        all_data.append(data_dict)

    return jsonify(all_data)



@app.route("/api/v1.0/houston311/ByMonth/zip/<zip_filter>/year/<year_filter>/neib/<neib_filter>/type/<type_filter>")
def houston311top10ByMonthZip(zip_filter, year_filter, neib_filter, type_filter):
    """Return a list of all weather for the state"""
    agg_sel = aggData
    if (zip_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['zipcode'] == str(zip_filter).strip()]
    if (year_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['yr'] == str(year_filter).strip()]
    if (neib_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['neighborhood'] == str(neib_filter).strip()]
    if (type_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['serv_type'] == str(type_filter).strip()]

    print('data in filter:'+ str(zip_filter), file=sys.stderr)
    aggTypes = agg_sel.groupby(['date_month']).agg(
    count_issues=('serv_type', 'count'),
    time_taken=('avg_time', 'mean'),
    overdue=('avg_overdue', 'mean'))
    weath_sel = weatherData
    if (year_filter != 'ALL'):
        weath_sel = weatherData[weatherData['yr'] == str(year_filter).strip()]

    weathAgg = weath_sel.groupby(['date_month']).agg(
    prec=('precipitation', 'sum'),
    avg_max=('tempMax', 'mean'))

    aggTypes.reset_index(inplace=True)
    weathAgg.reset_index(inplace=True)
    # aggTypes.sort_values('count_issues',ascending=False,inplace=True)
    # aggTypes = aggTypes.head(10)
    # close the session to end the communication with the database
    # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))
    all_data = []
    # for weather, index in weather_sel:
    for index, row in aggTypes.iterrows():
        data_dict = {}
        data_dict["sort_key"] = monthsDict[row.date_month]
        data_dict["date_month"] = row.date_month
        data_dict["count_issues"] = row.count_issues
        data_dict["time_taken"] = row.time_taken
        data_dict["overdue"] = row.overdue
        for index1, row1 in weathAgg.iterrows():
            if (row1.date_month == row.date_month):
                data_dict["prec"] = row1.prec
                data_dict["avg_max"] = row1.avg_max

        all_data.append(data_dict)
    #OrderedDict(sorted(all_data.items(),key =lambda x:months.index(x[0])))
    all_data = sorted(all_data, key = lambda i: (i['sort_key'])) 
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
