from flask import render_template, request
from app import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
import numpy as np
import pickle

df_merged = pd.read_csv("/Users/akuepper/Desktop/Insight/project/data/chlamydia_cdc_census.csv")
df_zipfips= pd.read_csv("/Users/akuepper/Desktop/Insight/project/data/ZIP_COUNTY_122014.csv", usecols={0,1})
df_zipcode = pd.read_csv("/Users/akuepper/Desktop/Insight/project/data/census_zipcode.csv")
zip2fips = dict(zip(df_zipfips["ZIP"], df_zipfips["COUNTY"]))
model = pickle.load(open("/Users/akuepper/Desktop/Insight/project/data/randomforest_params.pickle", "rb"))

gender_rate = {}
gender_factor = {}
gender_number = {}
gender_rate["Male"] = 278.4e-5
gender_rate["Female"] = 627.2e-5
gender_number["Male"] = 155651602
gender_number["Female"] = 160477237
rate_average = (gender_rate["Male"]*gender_number["Male"]+gender_rate["Female"]*gender_number["Male"])/(gender_number["Male"]+gender_number["Female"])
gender_factor["Male"] = gender_rate["Male"]/rate_average
gender_factor["Female"] = gender_rate["Female"]/rate_average
gender_factor["Female"], gender_factor["Male"]
race_rate = {}
race_factor = {}
race_number = {}
race_number["Native"] = 1942876.0
race_number["Asian"] = 12721721.0
race_number["Black"] = 29489649.0
race_number["Hispanic"] = 46407173.0
race_number["Multiple"] = 5145135.0
race_number["Pacific"] = 473703.0
race_number["White"] = 161443167.0
race_rate["Native"] = 689.1e-5
race_rate["Asian"] = 115.8e-5
race_rate["Black"] = 1152.6e-5
race_rate["Hispanic"] = 376.2e-5
race_rate["Multiple"] = 116.1e-5
race_rate["Pacific"] = 641.5e-5
race_rate["White"] = 187.0e-5
US_number = race_number["Native"] + race_number["Asian"] + race_number["Black"] + race_number["Hispanic"] + race_number["Multiple"] + race_number["Pacific"] + race_number["White"]
rate_average = (race_rate["Native"]*race_number["Native"]+race_rate["Asian"]*race_number["Asian"]+race_rate["Black"]*race_number["Black"]+race_rate["Hispanic"]*race_number["Hispanic"]+race_rate["Multiple"]*race_number["Multiple"]+race_rate["Pacific"]*race_number["Multiple"]+race_rate["White"]*race_number["White"])/US_number  
race_factor["Native"] = race_rate["Native"]/rate_average
race_factor["Asian"] = race_rate["Asian"]/rate_average
race_factor["Black"] = race_rate["Black"]/rate_average
race_factor["Hispanic"] = race_rate["Hispanic"]/rate_average
race_factor["Multiple"] = race_rate["Multiple"]/rate_average
race_factor["Pacific"] = race_rate["Pacific"]/rate_average
race_factor["White"] = race_rate["White"]/rate_average

age_rate = {}
age_factor = {}
age_number = {}
age_number["0-14"] = 61089123.0
age_number["15-19"] = 21158964.0
age_number["20-24"] = 22795438.0
age_number["25-29"] = 21580198.0
age_number["30-34"] = 21264389.0
age_number["35-39"] = 19603770.0
age_number["40-44"] = 20848920.0
age_number["45-54"] = 43767532.0
age_number["55-64"] = 39316431.0
age_number["65+"] = 44704074.0

age_rate["0-14"] = 20.0e-5
age_rate["15-19"] = 1804.0e-5
age_rate["20-24"] = 2484.6e-5
age_rate["25-29"] = 1176.2e-5
age_rate["30-34"] = 532.4e-5
age_rate["35-39"] = 268.0e-5
age_rate["40-44"] = 131.5e-5
age_rate["45-54"] = 56.6e-5
age_rate["55-64"] = 16.6e-5
age_rate["65+"] = 3.2e-5

US_age_number = age_number["0-14"] + age_number["15-19"] + age_number["20-24"] + age_number["25-29"] + age_number["30-34"] + age_number["35-39"] + age_number["40-44"] + age_number["45-54"] + age_number["55-64"] + age_number["65+"]
rate_average = (age_rate["0-14"]*age_number["0-14"]+age_rate["15-19"]*age_number["15-19"]+age_rate["20-24"]*age_number["20-24"]+age_rate["25-29"]*age_number["25-29"]+age_rate["30-34"]*age_number["30-34"]+age_rate["35-39"]*age_number["35-39"]+age_rate["40-44"]*age_number["40-44"]+age_rate["45-54"]*age_number["45-54"]+age_rate["55-64"]*age_number["55-64"]+age_rate["65+"]*age_number["65+"])/US_age_number  
age_factor["0-14"] = age_rate["0-14"]/rate_average
age_factor["15-19"] = age_rate["15-19"]/rate_average
age_factor["20-24"] = age_rate["20-24"]/rate_average
age_factor["25-29"] = age_rate["30-34"]/rate_average
age_factor["30-34"] = age_rate["30-34"]/rate_average
age_factor["35-39"] = age_rate["35-39"]/rate_average
age_factor["40-44"] = age_rate["40-44"]/rate_average
age_factor["45-54"] = age_rate["45-54"]/rate_average
age_factor["55-64"] = age_rate["55-64"]/rate_average
age_factor["65+"] = age_rate["65+"]/rate_average



def calculate_rate(Zipcode):
    target = df_zipcode[df_zipcode["geoid2"]==int(Zipcode)]

#    fips = zip2fips[int(Zipcode)]
#    target = df_merged[df_merged['FIPS']==fips]
    target_params = target.values[0]
    chlamydia_rate = model.predict(target_params[1:])
    return chlamydia_rate*100



@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
       title = 'Home', user = { 'nickname': 'Miguel' },
       )

@app.route('/db')
def birth_page():
    sql_query = """                                                             
                SELECT * FROM birth_data_table WHERE delivery_method='Cesarean'\
;                                                                               
                """
    query_results = pd.read_sql_query(sql_query,con)
    births = ""
    print(query_results[:10])
    for i in range(0,10):
        births += query_results.iloc[i]['birth_month']
        births += "<br>"
    return births


@app.route('/db_fancy')
def cesareans_page_fancy():
    sql_query = """
               SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean';
                """
    query_results=pd.read_sql_query(sql_query,con)
    births = []
    for i in range(0,query_results.shape[0]):
        births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
    return render_template('cesareans.html',births=births)


@app.route('/input')
def stdme_input():
    return render_template("input.html")


@app.route('/output')
def stdme_output():

  #pull information from input fields and store it
  age = request.args.get('age')
  gender = request.args.get('gender')
  ethnicity = request.args.get('ethnicity')
  zipcode = request.args.get('zipcode')

#  #just select the Cesareans  from the birth dtabase for the month that the user inputs
#  query = "SELECT index, attendant, birth_month FROM birth_data_table WHERE delivery_method='Cesarean' AND birth_month='%s'" % patient
#  print(query)
#  query_results=pd.read_sql_query(query,con)
#  print(query_results)
#  births = []
#  for i in range(0,query_results.shape[0]):
#      births.append(dict(index=query_results.iloc[i]['index'], attendant=query_results.iloc[i]['attendant'], birth_month=query_results.iloc[i]['birth_month']))
  local_rate = calculate_rate(zipcode)
  rate = local_rate*gender_factor[gender]*race_factor[ethnicity]*age_factor[age]  
  return render_template("output.html", the_result = np.round(rate[0],decimals=2), average = np.round(local_rate[0],decimals=2))

