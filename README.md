# Final-Project

# Team:  Are You in the Right Neighborhood?

### Team Members:  Ruby Mittal, Philip Wirth, Jeff Eickholt

#### Summary:  We used data from the City of Houston 311 sytem.  This is a system where citizens of Houston can submit question or report issues, such as a missed garbage pickup.  The date is logged when the issue is reported and a due date is assigned.  The date when the issue is closed is logged when resolved.  We wanted to see if socioeconomic factors or weather would affect whether the issues are closed by the due date or not.

### There were a lot of files used for this project.  Below are some key files:

##### /Notebooks/model_classification.ipynb:  Notebook used to develop Logistic Regresion model and KNN model. The Logistic Model was deployed.
##### app.py:  Flask applicaton.
##### /templates/index.html:  Main web page

### This Repo contains the following folders and files:

### Files:

##### HoustonCity.pptx:  Final presentation
##### Proposal.docx:  Initial Proposal
#####

### Folders:

#### Clean Data Files Folder Contains:  Cleaned up data files used in notebooks and app

###### 311latlngzipcodes.csv:  File used to map zipcodes to lat/lng.
###### COH_ZIPCODE.geojson:  City of Houston zip code list.
###### Houston 311 SR Types by Year.csv:  List of 311 service types by year.
###### WeatherUnderground.xls:  Weather data scraped from Weather Underground.
###### Weather_KIAHstation_2017-2020.xls:  Weather data from IAH station.
###### census_date.csv:  Census data at zipcode level pulled from Census API.
###### htownzipcensus.geojson:  Houston zipcodes.
###### modelstardata.csv:  Initial data for model.
###### recorddata.csv: ???
###### weatherdata.csv:  Cleaned up weather data file.

#### Notebooks Folder Contains:

###### COHZips.ipynb:  City of Houston zipcode analysis.
###### Modeling Notebook.ipynb:  Initial file used to create data for modeling.
###### Philip's Data Clean Up.ipynb:  Further processing of raw data and prep of single data set to be used for modeling.
###### Philip's Data Clean Up Ruby.ipynb:  Further processing of raw data used by Ruby to create files for Flask app.
###### Raw Data Import.ipynb:  Import and processing or raw data.
###### Raw Data Import_ruby.ipynb:  Further review of raw data by Ruby.
###### Raw Data_merge_weather.ipynb:  Merging weather data in with other data.
###### Ruby Data Clean Up.ipynb:  Ruby further work in clean-up file.
###### Ruby_Raw Data Import.ipynb: Ruby working on data import.
###### Weather Dataset Modification.ipynb:  Correcting an issue with weather data that was identified.
###### census_data.ipynb:  Pulling census data at zipcode level from API and putting into csv file.
###### final_weather_data.ipynb:  Processing of final weather data.
###### model_classification:  Notebook used to develop logistic and KNN model and output the logistic model for use in the Flask application.  

#### backup Folder Contains:  Backup of different version of app.

#### static/css Folder Contains:

###### css_ruby.css: Styling sheet used by Ruby.
###### style.css:  Additional styling.

#### static/data Folder Contains:

###### Final_selected_weather_data.csv:  Weather data used in Flask app.
###### agg_hist_311_data.csv:  311 data used in Flask app.
###### census_data.json:  Census data to be used in Flask app.
###### selected_weather_data_for_visual.csv:  Weather data used to create visualizations.

#### static/js Folder Contains:

###### 311.js:
###### app_analysis.js:
###### app_chart.js:
###### app_pred.js:
###### app_ruby.js:
###### app_top10chart.js:
###### config.js:
###### showchart.js:
###### shp.min.js:

#### static/models Folder Contains:

###### logistic_model.pkl: Saved logistic regression model.
###### scaler.pkl:  Saved scaler that was used in model development.  This was then used in the Flask app to scale the example data before feeding into the model and outputing the prediction.

#### static/py Folder Contains:

###### app.py:  Flask application

#### templates Folder Contains:

###### ?
