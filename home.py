#source:
# https://stackoverflow.com/questions/26198714/how-to-retrieve-mac-addresses-from-nearby-hosts-in-python

from datetime import datetime
from os import times_result
import nmap
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import datetime
import time
from pyasn1_modules.rfc2459 import X520dnQualifier 
import schedule 
from twilio.rest import Client 
import socket

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("IoT Cloud").worksheet('Home')

homestate = 0
late = 0
sent = 0

#This section decides the sampling rate 
period = 60
tries = 8
wait = period/tries

#code to check if connected to internet
REMOTE_SERVER = "one.one.one.one"
def is_connected(hostname):
  try:
    # see if we can resolve the host name -- tells us if there is a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except:
     pass
  return False

#lets us know if its in the period where we notify arrivals 
def check_time():
    now = datetime.datetime.now()

#scans network to see if my phone is there 
def check_if_home():
        print('starting process...')

        now = datetime.datetime.now()
        print(now)

        target_mac = '64:A2:F9:B7:5E:02'  #this number has been hidden for safety reasons      

        nm = nmap.PortScanner()
        nm.scan(hosts='192.168.0.1/24', arguments='-sP')

        host_list = nm.all_hosts()
        print('list of devices....')
        pprint(host_list)
        device_log = []
        for host in host_list:
                if  'mac' in nm[host]['addresses']:
                        print(host+' : '+nm[host]['addresses']['mac'])
                        if target_mac == nm[host]['addresses']['mac']:
                                print('Target Found')
                                device_log.append([now.year, now.month, now.day, now.hour, now.minute, 1])
                                break
        else:
                device_log.append([now.year, now.month, now.day, now.hour, now.minute, 0])

        return device_log


# updated to match the correct sampling frequency
def check_if_home2():
        global wait 
        
        homelog = [0]
        x=tries 

        print('starting process...')
        target_mac = '64:A2:F9:B7:5E:02'  

        now = datetime.datetime.now()
        print(now)

        nm = nmap.PortScanner()
        nm.scan(hosts='192.168.0.1/24', arguments='-sP') 

        while x>0:
            print(x)
            host_list = nm.all_hosts()
            print('list of devices....')
            pprint(host_list)
            for host in host_list:
                    if  'mac' in nm[host]['addresses']:
                            print(host+' : '+nm[host]['addresses']['mac'])
                            if target_mac == nm[host]['addresses']['mac']:
                                    print('Target Found')
                                    homelog.append
                                    homelog.append([now.year, now.month, now.day, now.hour, now.minute, 1])
                                    time.sleep(wait)
                                    x = x-1
            else:
                    homelog.append(0)
                    x = x- 1
            
        return homelog

def upload_data():
        device_log = []
        homelog = check_if_home()
        now = datetime.datetime.now()
        timestamp = time.time()


        if 1 in homelog:
            homestate = 1
        else:
            homestate = 0

        device_log.append([now.year, now.month, now.day, now.hour, now.minute, homestate, timestamp])
        print(device_log)

        sheet.insert_row(device_log[0])
        print('Uploaded!')

def sendtext():           
 
        account_sid = 'AC14f3f88f01da0e335e687d17d50eff6b' 
        auth_token = '8aee574fb6c623f4f896757d47f854c6' 
        client = Client(account_sid, auth_token) 
 
        message = client.messages.create( 
                                from_='whatsapp:+14155238886',  
                                body='Good evening, I am home!',      
                                to='whatsapp:+447775441720' 
                                ) 

        # print(message.sid)

def data_collection():

    while REMOTE_SERVER:

        try:
            pass
        #     device_log = check_if_home()
            upload_data()
            time.sleep(120)
        except:
            pass

    else:
        print('connection to network error!')
        time.sleep(60)
        is_connected()

def main():

    while REMOTE_SERVER:

        try:
            late = check_time()
            upload_data()
            if late == 1 and homestate == 1 and sent == 0:
                sendtext()
                sent = 1
        except:
            time.sleep(10)

    else:
        print('connection to network error!')
        time.sleep(60)
        is_connected()

data_collection()  #use this for regular data collection
# main()      #use his for the final version

