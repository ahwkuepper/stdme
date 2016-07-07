from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd

#DB properties and account information
dbname = 'small_census_zipcode_db'
username = 'XXX'
pswd = 'XXX'
engine = create_engine('postgresql://%s:%s@localhost/%s'%(username,pswd,dbname))

# create a database (if it doesn't exist)
if not database_exists(engine.url):
    create_database(engine.url)
print(database_exists(engine.url))

# load the normalized database from CSV
zipcensus = pd.DataFrame.from_csv('../project/data/census_zipcode.csv')

# insert data into database from Python
zipcensus.to_sql('zip_census_db', engine, if_exists='replace')

# load the unnormalized database from CSV
zipcensus_unnormalized = pd.DataFrame.from_csv('../project/data/census_zipcode_unnormalized.csv')

# insert data into database
zipcensus_unnormalized.to_sql('zip_census_unnormalized_db', engine, if_exists='replace')


#test the new database

#query:
con = None
con = psycopg2.connect(database = dbname, user = username, host='localhost', password=pswd)

sql_query = """
SELECT * FROM zip_census_unnormalized_db WHERE geoid2='602';
"""

data_from_sql = pd.read_sql_query(sql_query,con)
print(data_from_sql.Population[0])

# query:
sql_query = """
SELECT * FROM zip_census_db WHERE geoid2='602';
"""

data_from_sql = pd.read_sql_query(sql_query,con)
print(data_from_sql.Population[0])
