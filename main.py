import os
#from re import match
from random import randint
from flask import Flask, request
#from apscheduler.scheduler import Scheduler
from twilio.rest import TwilioRestClient
import twilio.twiml
import constants

account_sid = os.environ['TWILIO_SID']
#account_sid = "AC9cda9f49921253df4a0781b4318f4d23"
auth_token = os.environ['TWILIO_AUTH_TOKEN']
#auth_token = "82b0d956d668f10c8b2b6ce7195052ef"
#twilio_number = ""
twilio_number = os.environ['TWILIO_NUMBER']

client = TwilioRestClient(account_sid, auth_token)

app = Flask(__name__, static_url_path="")

#scheduler = Scheduler()

"""def isPhone(input):
    matches = match(input)
    if matches:
        return True
    else:
        return False
"""

#scheduler.add_job(myfunc, 'interval', minutes=2, id='my_job_id')
#scheduler.remove_job('my_job_id')


def prank_call(id):
    call = client.calls.create(
        url=constants.SERVER_LOC + "/twiml/prank_call"+str(randint(1,2))+".xml",
        to=target,
        from_=twilio_number,
        method="GET",
        status_callback=constants.SERVER_LOC + "/callStatus",
        status_callback_method="POST",
        status_events=["completed"]
    )

@app.route("/")
def home():
    #do nothing
    return "Do nothing"

@app.route("/addTarget", methods=["POST"])
def addTarget():
    if request.values.get("From") and request.values.get("Body"):
        #assume from Twilio
        from_ = request.values.get("From")
        target = request.values.get("Body")
        if target.lower() == "STOP":
            #scheduler.remove_job(from_)
            return "Cancelled"
        else:
            try:
                call = client.calls.create(
                    url=constants.SERVER_LOC + "/twiml/prank_call"+str(randint(1,2))+".xml",
                    to=target,
                    from_=twilio_number,
                    method="GET",
                    status_callback=constants.SERVER_LOC + "/callStatus",
                    status_callback_method="POST",
                    status_events=["completed"]
                )
                #scheduler.add_job(prank_call(target), 'interval', minutes=2, id=target)
                return "Success"
            except Exception:
                rejection = twilio.twiml.Response()
                rejection.message("Stop trying to break my app! Please give me just a phone number")
                print "Failure"
                return str(rejection)
    print "Failure"
    return "Failure"

@app.route("/callStatus", methods=["POST"])
def callStatus():
    called = request.values.get("Called")
    callStatus = request.values.get("CallStatus")

    if callStatus == "completed":
        print "Success"
    else:
        print "Failed :("
    return "Yay"

if __name__ == "__main__":
    app.run(debug=True)
