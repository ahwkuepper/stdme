from flask import render_template, request, send_file
from app import app
from io import BytesIO
import pandas as pd
import numpy as np
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

exec(open("app/constants.py").read())

#Seaborn options
sns.set(style="white", context="talk")
d_label = np.array(["You", "Your gender", "Your age group", "Your race / ethnicity", "Your location"])

#load csv files
df_zipcode = pd.read_csv("/Users/akuepper/Desktop/Insight/project/data/census_zipcode.csv")
df_zipcode_unnormalized = pd.read_csv("/Users/akuepper/Desktop/Insight/project/data/census_zipcode_unnormalized.csv")
model = pickle.load(open("/Users/akuepper/Desktop/Insight/project/data/randomforest_params.pickle", "rb"))
Ymean = pickle.load(open('/Users/akuepper/Desktop/Insight/project/data/Ymean.pickle', "rb"))
Ystd = pickle.load(open('/Users/akuepper/Desktop/Insight/project/data/Ystd.pickle', "rb"))
model_gonorrhea = pickle.load(open("/Users/akuepper/Desktop/Insight/project/data/randomforest_params_gonorrhea.pickle", "rb"))
Ymean_gonorrhea = pickle.load(open('/Users/akuepper/Desktop/Insight/project/data/Ymean_gonorrhea.pickle', "rb"))
Ystd_gonorrhea = pickle.load(open('/Users/akuepper/Desktop/Insight/project/data/Ystd_gonorrhea.pickle', "rb"))
model_syphilis = pickle.load(open("/Users/akuepper/Desktop/Insight/project/data/randomforest_params_syphilis.pickle", "rb"))
Ymean_syphilis = pickle.load(open('/Users/akuepper/Desktop/Insight/project/data/Ymean_syphilis.pickle', "rb"))
Ystd_syphilis = pickle.load(open('/Users/akuepper/Desktop/Insight/project/data/Ystd_syphilis.pickle', "rb"))

df_sites = pd.read_csv('/Users/akuepper/Desktop/Insight/project/data/testingsites.csv')


dbname = 'small_census_zipcode_db'
username = 'akuepper'
pswd = 'FLP@nd'
engine = create_engine('postgresql://%s:%s@localhost/%s'%(username,pswd,dbname))
con = None
con = psycopg2.connect(database = dbname, user = username, host='localhost', password=pswd)



def lookup_std_testing_site(Zipcode):
    clinic = df_sites[df_sites["zipcode"]==Zipcode].name.str.lstrip().str.rstrip().values
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
    sql_query = "SELECT * FROM zip_census_db WHERE geoid2=%i;"%(Zipcode)
    target = pd.read_sql_query(sql_query,con)
    target_params = target.values[0]
    chlamydia_rate = model.predict(target_params[1:])*Ystd+Ymean
    return chlamydia_rate

def calculate_rate_gonorrhea(Zipcode):
    sql_query = "SELECT * FROM zip_census_db WHERE geoid2=%i;"%(Zipcode)
    target = pd.read_sql_query(sql_query,con)
    target_params = target.values[0]
    gonorrhea_rate = model_gonorrhea.predict(target_params[1:])*Ystd_gonorrhea+Ymean_gonorrhea
    return gonorrhea_rate

def calculate_rate_syphilis(Zipcode):
    sql_query = "SELECT * FROM zip_census_db WHERE geoid2=%i;"%(Zipcode)
    target = pd.read_sql_query(sql_query,con)
    target_params = target.values[0]
    syphilis_rate = model_syphilis.predict(target_params[1:])*Ystd_syphilis+Ymean_syphilis
    return syphilis_rate


@app.route('/make_plot/you/<float:yourrate>/gender/<float:genderrate>/age/<float:agerate>/race/<float:racerate>/location/<float:locationrate>/national/<float:nationalrate>')
def make_plot(yourrate, genderrate, agerate, racerate, locationrate, nationalrate):  
  d = np.array([yourrate, genderrate, agerate, racerate, locationrate])
  fig, ax = plt.subplots(1, 1, figsize=(10, 6), sharex=True)
  sns.barplot(d_label, d, palette="RdBu_r", ax=ax)
  ax.axhline(nationalrate, alpha=0.5, color='black', ls='dotted')
  ax.set_ylabel('Risk', fontsize=25)
  sns.despine(bottom=True)
  plt.setp(fig.axes, yticks=[])
  plt.tight_layout(h_pad=3)
  img = BytesIO()
  fig.savefig(img)
  img.seek(0)
  return send_file(img, mimetype='image/png')


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")



@app.route('/output')
def stdme_output():

  #pull information from input fields and store it
  age = int(request.args.get('age'))
  zipcode_string = request.args.get('zipcode')
  zipcode = int(zipcode_string)
  gender = request.args.get('gender_select')
  race = request.args.get('race_select')
  
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

# get entry from SQL database
  sql_query = "SELECT * FROM zip_census_unnormalized_db WHERE geoid2=%i;"%(zipcode)
  target_unnormalized = pd.read_sql_query(sql_query,con)


  TOTALNR = target_unnormalized["Population"]+1.0

  if gender == "Male":
      gender_table = "hd02s026"
  else:
      gender_table = "hd02s051"

  GENDERNR = TOTALNR*target_unnormalized[gender_table]/100.0+1.0

  if race == "White":
      race_table = "hd02s078"
  elif race == "Black":
      race_table = "hd02s079"
  elif race == "Native":
      race_table = "hd02s080"
  elif race == "Asian":
      race_table = "hd02s081"
  elif race == "Pacific":
      race_table = "hd02s089"
  elif race == "Multiple":
      race_table = "hd02s095"
  elif race == "Hispanic":
      race_table = "hd02s107"

  RACENR = TOTALNR*target_unnormalized[race_table]/100.0+1.0

  if age == "0-14":
      age_table = "hd02s002"
  elif age == "15-19":
      age_table = "hd02s005"
  elif age == "20-24":
      age_table = "hd02s006"
  elif age == "25-29":
      age_table = "hd02s007"
  elif age == "30-34":
      age_table = "hd02s008"
  elif age == "35-39":
      age_table = "hd02s009"
  elif age == "40-44":
      age_table = "hd02s010"
  elif age == "45-54":
      age_table = "hd02s011"
  elif age == "55-64":
      age_table = "hd02s013"
  elif age == "65+":
      age_table = "hd02s015"

  AGENR = TOTALNR*target_unnormalized[age_table]/100.0+1.0

  zipcoderate = calculate_rate(zipcode)*100
  genderrate = gender_rate[gender]*100
  agerate = age_rate[age]*100
  racerate = race_rate[race]*100

  zipcoderate_gonorrhea = calculate_rate_gonorrhea(zipcode)*100
  genderrate_gonorrhea = gender_rate_gonorrhea[gender]*100
  agerate_gonorrhea = age_rate_gonorrhea[age]*100
  racerate_gonorrhea = race_rate_gonorrhea[race]*100

  zipcoderate_syphilis = calculate_rate_syphilis(zipcode)*100
  genderrate_syphilis = gender_rate_syphilis[gender]*100
  agerate_syphilis = age_rate_syphilis[age]*100
  racerate_syphilis = race_rate_syphilis[race]*100


  print("Chlamydia: ", zipcoderate, TOTALNR.values, genderrate, GENDERNR.values, racerate, RACENR.values, agerate, AGENR.values)
  print("Gonorrhea: ", zipcoderate_gonorrhea, TOTALNR.values, genderrate_gonorrhea, GENDERNR.values, racerate_gonorrhea, RACENR.values, agerate_gonorrhea, AGENR.values)
  print("Syphilis: ", zipcoderate_syphilis, TOTALNR.values, genderrate_syphilis, GENDERNR.values, racerate_syphilis, RACENR.values, agerate_syphilis, AGENR.values)

  the_result = (zipcoderate/TOTALNR.values + genderrate/GENDERNR.values + racerate/RACENR.values + agerate/AGENR.values)/(1.0/TOTALNR.values+1.0/GENDERNR.values+1.0/RACENR.values+1.0/AGENR.values)
  the_result_gonorrhea = (zipcoderate_gonorrhea/TOTALNR.values + genderrate_gonorrhea/GENDERNR.values + racerate_gonorrhea/RACENR.values + agerate_gonorrhea/AGENR.values)/(1.0/TOTALNR.values+1.0/GENDERNR.values+1.0/RACENR.values+1.0/AGENR.values)
  the_result_syphilis = (zipcoderate_syphilis/TOTALNR.values + genderrate_syphilis/GENDERNR.values + racerate_syphilis/RACENR.values + agerate_syphilis/AGENR.values)/(1.0/TOTALNR.values+1.0/GENDERNR.values+1.0/RACENR.values+1.0/AGENR.values)

  d = np.array([the_result[0], genderrate, agerate, racerate, zipcoderate[0]])
  d_gonorrhea = np.array([the_result_gonorrhea[0], genderrate_gonorrhea, agerate_gonorrhea, racerate_gonorrhea, zipcoderate_gonorrhea[0]])
  d_syphilis = np.array([the_result_syphilis[0], genderrate_syphilis, agerate_syphilis, racerate_syphilis, zipcoderate_syphilis[0]])
  
  sentence = lookup_std_testing_site(zipcode)

  if d[0]/(100*rate_average) > 3.0:
    warning = "VERY HIGH"
  elif d[0]/(100*rate_average) > 2.0:
    warning = "Very high"
  elif d[0]/(100*rate_average) > 1.0:
    warning = "High"
  else:
    warning = "Lower than average"

  nthperson = int(100.0/d[4])


  if d_gonorrhea[0]/(100*rate_average_gonorrhea) > 3.0:
    warning_gonorrhea = "VERY HIGH"
  elif d_gonorrhea[0]/(100*rate_average_gonorrhea) > 2.0:
    warning_gonorrhea = "Very high"
  elif d_gonorrhea[0]/(100*rate_average_gonorrhea) > 1.0:
    warning_gonorrhea = "High"
  else:
    warning_gonorrhea = "Lower than average"

  nthperson_gonorrhea = int(100.0/d_gonorrhea[4])


  if d_syphilis[0]/(100*rate_average_syphilis) > 3.0:
    warning_syphilis = "VERY HIGH"
  elif d_syphilis[0]/(100*rate_average_syphilis) > 2.0:
    warning_syphilis = "Very high"
  elif d_syphilis[0]/(100*rate_average_syphilis) > 1.0:
    warning_syphilis = "High"
  else:
    warning_syphilis = "Lower than average"

  nthperson_syphilis = int(100.0/d_syphilis[4])


  return render_template("output.html", the_result = np.round(the_result[0],decimals=2), average = np.round(zipcoderate[0],decimals=2), zipcode = zipcode_string, sentence = sentence, yourrate = d[0], genderrate = d[1], agerate = d[2], racerate = d[3], locationrate = d[4], warning = warning, nthperson = nthperson, national_average = np.round(rate_average*100, decimals=2), the_result_gonorrhea = np.round(the_result_gonorrhea[0],decimals=2), average_gonorrhea = np.round(zipcoderate_gonorrhea[0],decimals=2), yourrate_gonorrhea = d_gonorrhea[0], genderrate_gonorrhea = d_gonorrhea[1], agerate_gonorrhea = d_gonorrhea[2], racerate_gonorrhea = d_gonorrhea[3], locationrate_gonorrhea = d_gonorrhea[4], warning_gonorrhea = warning_gonorrhea, nthperson_gonorrhea = nthperson_gonorrhea, national_average_gonorrhea = np.round(rate_average_gonorrhea*100, decimals=2), the_result_syphilis = np.round(the_result_syphilis[0],decimals=2), average_syphilis = np.round(zipcoderate_syphilis[0],decimals=2), yourrate_syphilis = d_syphilis[0], genderrate_syphilis = d_syphilis[1], agerate_syphilis = d_syphilis[2], racerate_syphilis = d_syphilis[3], locationrate_syphilis = d_syphilis[4], warning_syphilis = warning_syphilis, nthperson_syphilis = nthperson_syphilis, national_average_syphilis = np.round(rate_average_syphilis*100, decimals=2))

