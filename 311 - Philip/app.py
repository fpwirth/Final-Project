# Docs on session basics

import numpy as np
import pandas as pd
import os
import pickle
from collections import OrderedDict
from sklearn.preprocessing import StandardScaler
from flask import Flask, jsonify, request, render_template

#################################################
# read data from the csv files
#################################################

# Save reference to the table
weatherData = pd.read_csv("static/data/selected_weather_data_for_visual.csv")
aggData = pd.read_csv("static/data/agg_hist_311_data.csv")
censusData = pd.read_json("static/data/census_data.json")
weatherData['date_field_str'] = weatherData['date_field_str'].astype('str')
weatherData['yr'] = weatherData['yr'].astype('str')
censusData['zipcode'] = censusData['Zipcode'].astype('str')
aggData['zipcode'] = aggData['zipcode'].astype('str')
aggData['yr'] = aggData['yr'].astype('str')
aggData['date_field_str'] = aggData['date_field_str'].astype('str')

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
monthsDict = {'Jan': 1,'Feb' : 2,'Mar': 3,'Apr': 4,'May': 5,'Jun': 6,'Jul': 7,'Aug': 8,'Sep': 9,'Oct': 10,'Nov': 11,'Dec': 12}

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Loaf Model
#################################################

def load_model():
    global model
    with open('static/models/logistic_model.pkl', 'rb') as f:
        model = pickle.load(f)
        print("model loaded")

#################################################
# Flask Routes
#################################################

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_data = request.form.to_dict()
        data = process_input(input_data)
        value = model.predict(data)
        return render_template('index.html', result=value)

    return render_template('index.html')

def process_input(data):
    zip_filter = data['selZip']
    type_filter = data['selType']
    temp_entered = data['selTemp']
    rain_entered = data['selRain']
    census_sel = censusData[censusData['zipcode'] == str(zip_filter).strip()]
    all_data = []
    data_dict = {}
    for index, census in census_sel.iterrows():
        population = census['Population']
        MedianAge = census['Median Age']
        HouseholdIncome = census['Household Income']
        PovertyRate = census['Poverty Rate']
        PerOwnerOccupied = census['% Owner Occupied']
        data_dict['MedianAge'] = census['Median Age']
        data_dict['HouseholdIncome'] = census['Household Income']
        data_dict["Population"] = census['Population']
        data_dict["PerCapitaIncome"] = census['Per Capita Income']
        data_dict["PovertyRate"] = census['Poverty Rate']
        data_dict["TotalHouseholds"] = census['Total Households']
        data_dict["TotalOwnerOccupied"] = census['Total Owner Occupied']
        data_dict["PerOwnerOccupied"] = census['% Owner Occupied']
    contProb = 0
    if (type_filter == 'Container Problem'):
        contProb = 1
    drainProb = 0
    if (type_filter == 'Drainage'):
        drainProb = 1
    missedGarbProb = 0
    if (type_filter == 'Missed Garbage Pickup'):
        missedGarbProb = 1
    missedHeavyProb = 0
    if (type_filter == 'Missed Heavy Trash Pickup'):
        missedHeavyProb = 1
    missedRecProb = 0
    if (type_filter == 'Missed Recycling Pickup'):
        missedRecProb = 1
    nuisProb = 0
    if (type_filter == 'Nuisance On Property'):
        nuisProb = 1
    smwProb = 0
    if (type_filter == 'SWM Escalation'):
        smwProb = 1
    sewerProb = 0
    if (type_filter == 'Sewer Wasterwater'):
        sewerProb = 1
    stormProb = 0
    if (type_filter == 'Storm Debris Collection'):
        stormProb = 1
    streetCondProb = 0
    if (type_filter == 'Street Condition'):
        streetCondProb = 1
    streetHazardProb = 0
    if (type_filter == 'Street Hazard'):
        streetHazardProb = 1
    traficSignalProb = 0
    if (type_filter == 'Traffic Signal Maintenance'):
        traficSignalProb = 1
    trafficSignProb = 0
    if (type_filter == 'Traffic Sign'):
        trafficSignProb = 1
    waterLeakProb = 0
    if (type_filter == 'Water Leak'):
        waterLeakProb = 1
    waterServiceProb = 0
    if (type_filter == 'Water Service'):
        waterServiceProb = 1

# Population, Median Age, Household Income, Poverty Rate, % Owner Occupied, tempAvg, precipAvg, Container Problem, Drainage,
# Missed Garbage Pickup, Missed Heavy Trash Pickup, Missed Recycling Pickup, Nuisance On Property, SWM Escalation, 
# Sewer Wasterwater, Storm Debris Collection, Street Condition,
# Street Hazard, Traffic Signal Maintenance, Traffic Sign, Water Leak, Water Service

    new_data = [[population, MedianAge, HouseholdIncome, 
                PovertyRate, PerOwnerOccupied, float(temp_entered), float(rain_entered),
                contProb, drainProb, missedGarbProb, missedHeavyProb, 
                missedRecProb, nuisProb, smwProb, sewerProb, 
                stormProb, streetCondProb, streetHazardProb, traficSignalProb, 
                trafficSignProb, waterLeakProb, waterServiceProb]]
    print(new_data)
    X_scaler = StandardScaler().fit(new_data)
    data_scaled = X_scaler.transform(new_data)
    print(data_scaled)
    return data_scaled

@app.route("/api/v1.0/weather/date/<date_filter>")
def stateData(date_filter):
    weather_sel = weatherData[weatherData['date_field_str'] == str(date_filter).strip()]
    all_data = []
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
    census_sel = censusData[censusData['zipcode'] == str(zipcode_filter).strip()]
    all_data = []
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
    allZips = aggData.zipcode.unique()
    return jsonify(allZips.tolist())

@app.route("/api/v1.0/getAllTypes")
def getAllTypes():
    allServs = aggData.serv_type.unique()
    return jsonify(allServs.tolist())

@app.route("/api/v1.0/getAllDates")
def getAllDates():
    allDates = aggData.date_field_str.unique()
    return jsonify(allDates.tolist())

@app.route("/api/v1.0/getAllNeib")
def getAllNeib():
    allDates = aggData.neighborhood.unique()
    return jsonify(allDates.tolist())

@app.route("/api/v1.0/houston311/zipcode/date/type/<zipcode_filter>/<date_filter>/<type_filter>")
def houston311byAll(zipcode_filter, date_filter, type_filter):
    agg_sel = aggData[aggData['zipcode'] == str(zipcode_filter).strip()]
    agg_sel = agg_sel[agg_sel['date_field_str'] == str(date_filter).strip()]
    agg_sel = agg_sel[agg_sel['serv_type'] == str(type_filter).strip()]
    all_data = []
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
    aggTypes = aggData.groupby(['serv_type']).agg(
    count_issues=('serv_type', 'count'))  
    aggTypes.reset_index(inplace=True)
    aggTypes.sort_values('count_issues',ascending=False,inplace=True)
    aggTypes = aggTypes.head(10)
    all_data = []
    for index, row in aggTypes.iterrows():
        data_dict = {}
        data_dict["serv_type"] = row.serv_type
        data_dict["count_issues"] = row.count_issues
        all_data.append(data_dict)
    return jsonify(all_data)

@app.route("/api/v1.0/houston311/ByMonth")
def houston311top10ByMonth():
    aggTypes = aggData.groupby(['date_month']).agg(
    count_issues=('serv_type', 'count')) 
    weathAgg = weatherData.groupby(['date_month']).agg(
    prec=('precipitation', 'sum'),
    avg_max=('tempMax', 'mean'))
    aggTypes.reset_index(inplace=True)
    weathAgg.reset_index(inplace=True)
    all_data = []
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
def houston311Top10byZip(zip_filter, year_filter, neib_filter,  type_filter):
    agg_sel = aggData
    if (zip_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['zipcode'] == str(zip_filter).strip()]
    if (year_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['yr'] == str(year_filter).strip()]
    if (neib_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['neighborhood'] == str(neib_filter).strip()]
    if (type_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['serv_type'] == str(type_filter).strip()]
    aggTypes = agg_sel.groupby(['serv_type']).agg(
    count_issues=('serv_type', 'count'))  
    aggTypes.reset_index(inplace=True)
    aggTypes.sort_values('count_issues',ascending=False,inplace=True)
    aggTypes = aggTypes.head(10)
    all_data = []
    for index, row in aggTypes.iterrows():
        data_dict = {}
        data_dict["serv_type"] = row.serv_type
        data_dict["count_issues"] = row.count_issues
        all_data.append(data_dict)
    return jsonify(all_data)

@app.route("/api/v1.0/houston311/ByMonth/zip/<zip_filter>/year/<year_filter>/neib/<neib_filter>/type/<type_filter>")
def houston311top10ByMonthZip(zip_filter, year_filter, neib_filter, type_filter):
    agg_sel = aggData
    if (zip_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['zipcode'] == str(zip_filter).strip()]
    if (year_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['yr'] == str(year_filter).strip()]
    if (neib_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['neighborhood'] == str(neib_filter).strip()]
    if (type_filter != 'ALL'):
        agg_sel = agg_sel[agg_sel['serv_type'] == str(type_filter).strip()]
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
    all_data = []
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
    all_data = sorted(all_data, key = lambda i: (i['sort_key'])) 
    return jsonify(all_data)

if __name__ == '__main__':
    load_model()
    app.run(debug=True)
