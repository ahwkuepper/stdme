from flask import render_template, request
from app import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2
import numpy as np
import pickle

df_zipcode = pd.read_csv("/Users/akuepper/Desktop/Insight/project/data/census_zipcode.csv")
model = pickle.load(open("/Users/akuepper/Desktop/Insight/project/data/randomforest_params.pickle", "rb"))
Ymean = pickle.load(open('/Users/akuepper/Desktop/Insight/project/data/Ymean.pickle', "rb"))
Ystd = pickle.load(open('/Users/akuepper/Desktop/Insight/project/data/Ystd.pickle', "rb"))

df_sites = pd.read_csv('/Users/akuepper/Desktop/Insight/project/data/testingsites.csv')

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


def lookup_std_testing_site(Zipcode):
    clinic = df_sites[df_sites["zipcode"]==int(Zipcode)].name.str.lstrip().str.rstrip().values
    if len(clinic):
        words = clinic[0].split()
    else:
        words = "free STD testing near"
        words = words.split()
    for word in np.arange(len(words)):
        if word == 0:
            sentence = words[0]
        else:
            sentence = sentence + "+" + words[word]
    return sentence


def calculate_rate(Zipcode):
    target = df_zipcode[df_zipcode["geoid2"]==int(Zipcode)]
    target_params = target.values[0]
    chlamydia_rate = model.predict(target_params[1:])*Ystd+Ymean
    return chlamydia_rate*100


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


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


@app.route('/output')
def stdme_output():

  #pull information from input fields and store it
  age = request.args.get('age')
  zipcode = request.args.get('zipcode')
  gender = request.args.get('gender_select')
  ethnicity = request.args.get('ethnicity_select')
  
  if int(age) > 64:
    age = "65+"
  elif int(age) > 54:
    age = "55-64"
  elif int(age) > 44:
    age = "45-54"
  elif int(age) > 39:
    age = "40-44"
  elif int(age) > 34:
    age = "35-39"
  elif int(age) > 29:
    age = "30-34"
  elif int(age) > 24:
    age = "25-29"
  elif int(age) > 19:
    age = "20-24"
  elif int(age) > 14:
    age = "15-19"
  else:
    age = "0-14"

  print(ethnicity)

  local_rate = calculate_rate(zipcode)
  rate = local_rate*gender_factor[gender]*race_factor[ethnicity]*age_factor[age]  

  sentence = lookup_std_testing_site(zipcode)

  return render_template("output.html", the_result = np.round(rate[0],decimals=2), average = np.round(local_rate[0],decimals=2), zipcode = zipcode, sentence = sentence)

