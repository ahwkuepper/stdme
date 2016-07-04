#labels for summary plots
d_label = np.array(["You", "Your gender", "Your age group", "Your race / ethnicity", "Your location"])

#US statistics
gender_number = {}

gender_number["Male"] = 155651602
gender_number["Female"] = 160477237

race_number = {}

race_number["Native"] = 1942876.0
race_number["Asian"] = 12721721.0
race_number["Black"] = 29489649.0
race_number["Hispanic"] = 46407173.0
race_number["Multiple"] = 5145135.0
race_number["Pacific"] = 473703.0
race_number["White"] = 161443167.0

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



#Chlamydia statistics
gender_rate = {}
gender_factor = {}

gender_rate["Male"] = 278.4e-5
gender_rate["Female"] = 627.2e-5

rate_average = (gender_rate["Male"]*gender_number["Male"]+gender_rate["Female"]*gender_number["Male"])/(gender_number["Male"]+gender_number["Female"])

gender_factor["Male"] = gender_rate["Male"]/rate_average
gender_factor["Female"] = gender_rate["Female"]/rate_average
gender_factor["Female"], gender_factor["Male"]

race_rate = {}
race_factor = {}

race_rate["Native"] = 689.1e-5
race_rate["Asian"] = 115.8e-5
race_rate["Black"] = 1152.6e-5
race_rate["Hispanic"] = 376.2e-5
race_rate["Multiple"] = 116.1e-5
race_rate["Pacific"] = 641.5e-5
race_rate["White"] = 187.0e-5

race_factor["Native"] = race_rate["Native"]/rate_average
race_factor["Asian"] = race_rate["Asian"]/rate_average
race_factor["Black"] = race_rate["Black"]/rate_average
race_factor["Hispanic"] = race_rate["Hispanic"]/rate_average
race_factor["Multiple"] = race_rate["Multiple"]/rate_average
race_factor["Pacific"] = race_rate["Pacific"]/rate_average
race_factor["White"] = race_rate["White"]/rate_average

age_rate = {}
age_factor = {}

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

age_factor["0-14"] = age_rate["0-14"]/rate_average
age_factor["15-19"] = age_rate["15-19"]/rate_average
age_factor["20-24"] = age_rate["20-24"]/rate_average
age_factor["25-29"] = age_rate["25-29"]/rate_average
age_factor["30-34"] = age_rate["30-34"]/rate_average
age_factor["35-39"] = age_rate["35-39"]/rate_average
age_factor["40-44"] = age_rate["40-44"]/rate_average
age_factor["45-54"] = age_rate["45-54"]/rate_average
age_factor["55-64"] = age_rate["55-64"]/rate_average
age_factor["65+"] = age_rate["65+"]/rate_average


#Gonorrhea statistics
gender_rate_gonorrhea = {}
gender_factor_gonorrhea = {}

gender_rate_gonorrhea["Male"] = 120.1e-5
gender_rate_gonorrhea["Female"] = 101.3e-5

rate_average_gonorrhea = (gender_rate_gonorrhea["Male"]*gender_number["Male"]+gender_rate_gonorrhea["Female"]*gender_number["Male"])/(gender_number["Male"]+gender_number["Female"])

gender_factor_gonorrhea["Male"] = gender_rate_gonorrhea["Male"]/rate_average
gender_factor_gonorrhea["Female"] = gender_rate_gonorrhea["Female"]/rate_average
gender_factor_gonorrhea["Female"], gender_factor["Male"]

race_rate_gonorrhea = {}
race_factor_gonorrhea = {}

race_rate_gonorrhea["Native"] = 103.2e-5
race_rate_gonorrhea["Asian"] = 19.9e-5
race_rate_gonorrhea["Black"] = 422.9e-5
race_rate_gonorrhea["Hispanic"] = 72.7e-5
race_rate_gonorrhea["Multiple"] = 39.1e-5
race_rate_gonorrhea["Pacific"] = 103.2e-5
race_rate_gonorrhea["White"] = 39.8e-5

race_factor_gonorrhea["Native"] = race_rate_gonorrhea["Native"]/rate_average_gonorrhea
race_factor_gonorrhea["Asian"] = race_rate_gonorrhea["Asian"]/rate_average_gonorrhea
race_factor_gonorrhea["Black"] = race_rate_gonorrhea["Black"]/rate_average_gonorrhea
race_factor_gonorrhea["Hispanic"] = race_rate_gonorrhea["Hispanic"]/rate_average_gonorrhea
race_factor_gonorrhea["Multiple"] = race_rate_gonorrhea["Multiple"]/rate_average_gonorrhea
race_factor_gonorrhea["Pacific"] = race_rate_gonorrhea["Pacific"]/rate_average_gonorrhea
race_factor_gonorrhea["White"] = race_rate_gonorrhea["White"]/rate_average_gonorrhea

age_rate_gonorrhea = {}
age_factor_gonorrhea = {}

age_rate_gonorrhea["0-14"] = 4.3e-5
age_rate_gonorrhea["15-19"] = 323.6e-5
age_rate_gonorrhea["20-24"] = 509.8e-5
age_rate_gonorrhea["25-29"] = 322.5e-5
age_rate_gonorrhea["30-34"] = 180.6e-5
age_rate_gonorrhea["35-39"] = 106.1e-5
age_rate_gonorrhea["40-44"] = 60.9e-5
age_rate_gonorrhea["45-54"] = 35.0e-5
age_rate_gonorrhea["55-64"] = 11.6e-5
age_rate_gonorrhea["65+"] = 2.0e-5

age_factor_gonorrhea["0-14"] = age_rate_gonorrhea["0-14"]/rate_average_gonorrhea
age_factor_gonorrhea["15-19"] = age_rate_gonorrhea["15-19"]/rate_average_gonorrhea
age_factor_gonorrhea["20-24"] = age_rate_gonorrhea["20-24"]/rate_average_gonorrhea
age_factor_gonorrhea["25-29"] = age_rate_gonorrhea["25-29"]/rate_average_gonorrhea
age_factor_gonorrhea["30-34"] = age_rate_gonorrhea["30-34"]/rate_average_gonorrhea
age_factor_gonorrhea["35-39"] = age_rate_gonorrhea["35-39"]/rate_average_gonorrhea
age_factor_gonorrhea["40-44"] = age_rate_gonorrhea["40-44"]/rate_average_gonorrhea
age_factor_gonorrhea["45-54"] = age_rate_gonorrhea["45-54"]/rate_average_gonorrhea
age_factor_gonorrhea["55-64"] = age_rate_gonorrhea["55-64"]/rate_average_gonorrhea
age_factor_gonorrhea["65+"] = age_rate_gonorrhea["65+"]/rate_average_gonorrhea


#Syphilis statistics
gender_rate_syphilis = {}
gender_factor_syphilis = {}

gender_rate_syphilis["Male"] = 11.7e-5
gender_rate_syphilis["Female"] = 1.1e-5

rate_average_syphilis = (gender_rate_syphilis["Male"]*gender_number["Male"]+gender_rate_syphilis["Female"]*gender_number["Male"])/(gender_number["Male"]+gender_number["Female"])

gender_factor_syphilis["Male"] = gender_rate_syphilis["Male"]/rate_average
gender_factor_syphilis["Female"] = gender_rate_syphilis["Female"]/rate_average
gender_factor_syphilis["Female"], gender_factor["Male"]

race_rate_syphilis = {}
race_factor_syphilis = {}

race_rate_syphilis["Native"] = 7.9e-5
race_rate_syphilis["Asian"] = 2.8e-5
race_rate_syphilis["Black"] = 18.9e-5
race_rate_syphilis["Hispanic"] = 7.4e-5
race_rate_syphilis["Multiple"] = 2.3e-5
race_rate_syphilis["Pacific"] = 6.7e-5
race_rate_syphilis["White"] = 3.4e-5

race_factor_syphilis["Native"] = race_rate_syphilis["Native"]/rate_average_syphilis
race_factor_syphilis["Asian"] = race_rate_syphilis["Asian"]/rate_average_syphilis
race_factor_syphilis["Black"] = race_rate_syphilis["Black"]/rate_average_syphilis
race_factor_syphilis["Hispanic"] = race_rate_syphilis["Hispanic"]/rate_average_syphilis
race_factor_syphilis["Multiple"] = race_rate_syphilis["Multiple"]/rate_average_syphilis
race_factor_syphilis["Pacific"] = race_rate_syphilis["Pacific"]/rate_average_syphilis
race_factor_syphilis["White"] = race_rate_syphilis["White"]/rate_average_syphilis

age_rate_syphilis = {}
age_factor_syphilis = {}

age_rate_syphilis["0-14"] = 0.0e-5
age_rate_syphilis["15-19"] = 4.8e-5
age_rate_syphilis["20-24"] = 18.1e-5
age_rate_syphilis["25-29"] = 19.0e-5
age_rate_syphilis["30-34"] = 13.6e-5
age_rate_syphilis["35-39"] = 10.4e-5
age_rate_syphilis["40-44"] = 8.4e-5
age_rate_syphilis["45-54"] = 6.8e-5
age_rate_syphilis["55-64"] = 2.3e-5
age_rate_syphilis["65+"] = 0.4e-5

age_factor_syphilis["0-14"] = age_rate_syphilis["0-14"]/rate_average_syphilis
age_factor_syphilis["15-19"] = age_rate_syphilis["15-19"]/rate_average_syphilis
age_factor_syphilis["20-24"] = age_rate_syphilis["20-24"]/rate_average_syphilis
age_factor_syphilis["25-29"] = age_rate_syphilis["25-29"]/rate_average_syphilis
age_factor_syphilis["30-34"] = age_rate_syphilis["30-34"]/rate_average_syphilis
age_factor_syphilis["35-39"] = age_rate_syphilis["35-39"]/rate_average_syphilis
age_factor_syphilis["40-44"] = age_rate_syphilis["40-44"]/rate_average_syphilis
age_factor_syphilis["45-54"] = age_rate_syphilis["45-54"]/rate_average_syphilis
age_factor_syphilis["55-64"] = age_rate_syphilis["55-64"]/rate_average_syphilis
age_factor_syphilis["65+"] = age_rate_syphilis["65+"]/rate_average_syphilis



