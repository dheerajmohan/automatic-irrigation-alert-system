#!/usr/bin/python


import RPi.GPIO as GPIO # This is the GPIO library we need to use the GPIO pins on the Raspberry Pi
import time # This is the time library, we need this so we can use the sleep function
import requests

url = "https://www.fast2sms.com/dev/bulk"
headers = {
'authorization': "12Ci3obr8sPpz4q0UuHELIWB7m9Xawt5SGxVfDe6ThJdKOkYgynckhlP6grHQvsw9UB8SzbuAe2iCLWx",
'Content-Type': "application/x-www-form-urlencoded",
'Cache-Control': "no-cache",
}

def sendMessage(message):
    payload = "sender_id=FSTSMS&message="+message+"&language=english&route=p&numbers=7012049065,8606667384,7012264191,9495022580"
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

# This is our callback function, this function will be called every time there is a change on the specified GPIO channel, in this example we are using 17

def callback(channel):
    print(GPIO.input(channel))
    if GPIO.input(channel):
        print ("LED off")
        sendMessage("EVS Demo: Low water level! Water the plant immediately!!")
    else:
        print ("LED on")
        sendMessage("EVS Demo: Water level back to normal")

# Set our GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin that we have our digital output from our sensor connected to
channel = 17
# Set the GPIO pin to an input
GPIO.setup(channel, GPIO.IN)

# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
GPIO.add_event_callback(channel, callback)
