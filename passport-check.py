# Importing libraries
import time
import hashlib
import random
from datetime import datetime
from urllib.request import urlopen, Request
import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

yourPhone = ''  # The number you want the text to send to
twilioNumber = ''  # The number twilio has given you
testUrl = 'https://www.passport.service.gov.uk/urgent/'  # This is set to the gov passport service site but you could easily change this to anything else

client = Client(account_sid, auth_token)

# setting the URL you want to monitor
url = Request(testUrl, headers={'User-Agent': 'Mozilla/5.0'})

# perform a GET request and load the content of the website and store it in a var
response = urlopen(url).read()

# Create the initial hash
currentHash = hashlib.sha224(response).hexdigest()
print("Running application for:" + testUrl)
alert_message = 'Appointments are live. Go to ' + testUrl

#Initial pause
time.sleep(2)

def sendNotification(pre_message):
    message = client.messages \
        .create(
            body= pre_message + alert_message,
            from_=twilioNumber,
            to=yourPhone
        )
    print(message.sid)

while True:
    try:
        # perform the get request and store it in a var
        response = urlopen(url).read()

        # create a hash
        currentHash = hashlib.sha224(response).hexdigest()

        # wait for random amount of time between 30 seconds and 2 minutes
        time.sleep(random.randint(33, 60))

        # perform the get request
        response = urlopen(url).read()

        # create a new hash
        newHash = hashlib.sha224(response).hexdigest()

        # check if new hash is same as the previous hash
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        if newHash == currentHash:
            print("Nothing changed ", current_time)
            continue

        # if something changed in the hashes
        else:
            # notify
            print("Website changed", current_time)
            sendNotification("")
            print("App closed")
            quit()

    # To handle exceptions
    except Exception as e:
        print("error", current_time)
        sendNotification("Error: ")
        print("App closed")
        quit()
