#refrences:
# https://simonprickett.dev/playing-with-raspberry-pi-door-sensor-fun/

from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import datetime
import time 
from twilio.rest import Client 
import socket
from gpiozero import LED
from time import sleep
import RPi.GPIO as GPIO
import time
import sys
import signal 

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("IoT Cloud").worksheet('Door')

period = 120   #upload every 2 minutes
tries = 60     
wait = period/tries    #check every 2 seconds

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
    return True
  except:
     pass
  return False

def check_door():
    x = tries
    DOOR_SENSOR_PIN = 18

    door_log = []

    # Set Broadcom mode so we can address GPIO pins by number.
    GPIO.setmode(GPIO.BCM) 

    # Initially we don't know if the door sensor is open or closed...
    isOpen = None 

    # Set up the door sensor pin.
    GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP) 

    isOpen = GPIO.input(DOOR_SENSOR_PIN)

    while x>0:
        if isOpen:  
            print ("Door is Closed")
            door_log.append(0)
            time.sleep(wait)
        elif not isOpen:  
            print ("Door is open")
            door_log.append(1)
            time.sleep(wait)
        x = x-1
    
    print(door_log)
    return door_log

def upload_data():
    device_log = []
    door_log = check_door()
    now = datetime.datetime.now()
    print(now)
    timestamp = time.time()

    sheet = client.open("IoT Cloud").worksheet("Door")

    if 1 in door_log:
        doorstate = 1
    else:
        doorstate = 0
    
    device_log.append([now.year, now.month, now.day, now.hour, now.minute, doorstate, timestamp])
    print(device_log[0])
    sheet.insert_row(device_log[0])
    print('uploaded!')

def data_collection():
    
    while is_connected(REMOTE_SERVER):

        try:
            upload_data()
        except:
            print('DOOR ERROR')
            time.sleep(10)

    else:
        print('connection to internet failed')
        time.sleep(60)
        is_connected()


def main():

    while is_connected(REMOTE_SERVER):

        try:
            check_door()
            upload_data()
        except:
            print('DOOR ERROR')
            time.sleep(10)


    else:
        print('connection to internet failed')
        time.sleep(60)
        is_connected()

# data_collection()  #use this for regular data collection
# main()      #use his for the final version

upload_data()
