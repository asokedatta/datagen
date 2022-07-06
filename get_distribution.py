import os,sys
import pandas as pd

# Files path
PLACES = "/home/tigergraph/bi-sf100-composite-projected-fk/graphs/csv/bi/composite-projected-fk/initial_snapshot/static/Place/"
PERSON_IN_CITY = "/home/tigergraph/bi-sf100-composite-projected-fk/graphs/csv/bi/composite-projected-fk/initial_snapshot/dynamic/Person_isLocatedIn_City/" 
PARTOF_OF_PLACES = "/home/tigergraph/bi-sf100-composite-projected-fk/graphs/csv/bi/composite-projected-fk/initial_snapshot/static/Place_isPartOf_Place/"


# Read places
cities, countries, continents = {}, {}, {}

files = os.listdir(PLACES)
for file in files:
    for line in open(PLACES + file,'r').readlines():
        line = line.strip().split('|')
        if line[3] == "Country" : 
            countries[line[0]] = line[1]
        elif line[3] == "City" : cities[line[0]] = line[1]
        elif line[3] == "Continent" : continents[line[0]] = line[1] 


# Read Place part of a place
county_city = {}
files = os.listdir(PARTOF_OF_PLACES)
for file in files:
    for line in open(PARTOF_OF_PLACES + file,'r').readlines():
        line = line.strip().split('|')
        if line[1] in countries:
            if line[1] in county_city : county_city[line[1]].append(line[0])
            else  :  county_city[line[1]] = [line[0]]

# for key, val in county_city.items():
#     print(countries[key],len(val))


# Read Person located in city
city_NumOfPerson = {}
files = os.listdir(PERSON_IN_CITY)
for file in files:
    for line in open(PERSON_IN_CITY+file,'r').readlines():
        line = line.strip().split('|')
        if line[2] in city_NumOfPerson: city_NumOfPerson[line[2]] += 1
        else : city_NumOfPerson[line[2]] = 1


country_NumOfPerson = {}
for cityId, NumOfPerson in city_NumOfPerson.items():
    for countryId, cities in county_city.items():
        if cityId in cities:
            if countryId in country_NumOfPerson : country_NumOfPerson[countryId] += NumOfPerson
            else :  country_NumOfPerson[countryId] = NumOfPerson

totalPerson = 0
for key , val in country_NumOfPerson.items() :
    print(countries[key] , ',' , val)
    totalPerson += val

print(totalPerson)