from urllib.request import urlopen as uReq
from config import *
from bs4 import BeautifulSoup as soup
from twilio.rest import Client
from datetime import datetime
import time


def GetDoorStatus():

    url = PicoW()
    client = Client(account_sid(), auth_token())


    old_state = []

    new_state = []

    while True:
        try:
            uClient = uReq(url)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html, "html.parser")

            GetDoorStatus = page_soup.find_all("p", {"class": "state"})
            split_string =GetDoorStatus[0].text.split(",", 1)
            new_state = split_string[0].lower()
            
            cTime = datetime.now()
            Timestamp = cTime.strftime("%Y-%m-%d %H:%M:%S")
            
            if old_state != new_state:

                message = client.messages.create(from_=f'whatsapp:{twilio_phonenumber()}',body=f'Deur is {new_state}\n{Timestamp}',to=f'whatsapp:{my_phonenumber()}')
                print(f"Deur is {new_state} - {Timestamp}")
                print(f"{message.sid}\n")
                
                with open("./Logs/status.log", "a") as status:
                    status.write(f"Deur is {new_state} - {Timestamp}\n")
                
                old_state = new_state
                
            time.sleep(5)
        except:
            
            message = client.messages.create(from_=f'whatsapp:{twilio_phonenumber()}',body=f'*Script is broken*\n{Timestamp}',to=f'whatsapp:{my_phonenumber()}')
            print(f"Script Error - {Timestamp}")
            print(f"{message.sid}\n")
            
            with open("./Logs/errors.log", "a") as errors:
                errors.write(f"Script Error - {Timestamp}\n")
            break

GetDoorStatus()
