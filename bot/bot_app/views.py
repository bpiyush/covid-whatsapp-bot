from os.path import splitext

from geopy.geocoders import Nominatim

from django.shortcuts import render

# Create your views here.
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def get_location_from_zip(incoming_msg, return_location=True):
    splits = incoming_msg.split(' ')
    if len(splits) != 2:
        return  "Incorrect ZIP information entered. Please enter in the format: ZIP <your-zip-code>", None

    zipcode = splits[-1]
    if len(zipcode) != 6:
        return f"Incorrect ZIP code entered ({zipcode}). ZIP code should be 6 numbers, e.g., 422008.", None

    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(zipcode)

    return f"Thanks. Your location is {location}", location



@csrf_exempt
def index(request):
    if request.method == 'POST':
        # retrieve incoming message from POST request in lowercase
        incoming_msg = request.POST['Body'].lower()

        # create Twilio XML response
        resp = MessagingResponse()
        msg = resp.message()

        if incoming_msg == 'hello':
            response = "*Hi! Thanks for contacting COVID Helper Bot*. \
            \n Please enter your ZIP code in the format: ZIP <your-zip-code>."
            msg.body(response)

        elif incoming_msg.startswith('zip'):
            response, location = get_location_from_zip(incoming_msg)
            msg.body(response)

        return HttpResponse(str(resp))