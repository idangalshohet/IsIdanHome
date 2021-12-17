# sources:
# https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
# https://openweathermap.org/current

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import datetime
import time 
import schedule 
import requests
import json
import pprint
import socket

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("IoT Cloud").worksheet('Weather')


REMOTE_SERVER = "one.one.one.one"
def is_connected(hostname):
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(hostname)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        s.close()
        print("connected!")
        return True
    except:
        pass
        print("no internet!")
        return False


def check_weather():
    kelvin = 273.15
    # Enter your API key here
    api_key = "43d4c029dc859ac2961d06e2275cb159"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Give city name
    city_name = 'London'

    # complete_url variable to store
    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # get method of requests module
    # return response object
    response = requests.get(complete_url)

    # json method of response object
    # convert json format data into
    # python format data
    x = response.json()


    # Now x contains list of nested dictionaries
    # Check the value of "cod" key is equal to
    # "404", means city is found otherwise,
    # city is not found
    if x["cod"] != "404":
        
        y = x["main"]
        # print(y)
        z = x["weather"]
        # print(z)
        
        current_temperature = y["temp"] - kelvin   #gets temperature and converts to celcius
        current_conditions = z[0]["main"]

    return current_temperature, current_conditions

def upload_data():
    weather_log = []
    temp, condition = check_weather()
    print(type(condition))
    now = datetime.datetime.now()
    print(now)

    timestamp = time.time()

    weather_log.append([now.year, now.month, now.day, now.hour, now.minute, temp, condition, timestamp])
    sheet.insert_row(weather_log[0])
    print('uploaded!')


def data_collection():

    while is_connected():

        try:
            upload_data()
            time.sleep(60*60)
        except:
            print('WEATHER ERROR')
            time.sleep(10)
    
    else:
        print('connection to internet failed')
        time.sleep(60)
        is_connected()

def main():

    while is_connected(REMOTE_SERVER):

        try:
            upload_data()
            time.sleep(60*60)
        except:
            print('WEATHER ERROR')
            time.sleep(10)
                
    else:
        print('connection to internet failed')
        time.sleep(60)
        is_connected()

# data_collection()  #use this for regular data collection
main()      #use his for the final version

