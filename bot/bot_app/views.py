from os.path import splitext

from geopy.geocoders import Nominatim

from django.shortcuts import render

# Create your views here.
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import sys
sys.path.append('/Users/piyushbagad/personal/projects/covid-whatsapp-bot/')

from data.gsheets import get_gsheet

gsheet = get_gsheet()


def get_location_from_zip(incoming_msg, return_location=True):
    splits = incoming_msg.split(' ')
    if len(splits) != 2:
        return  "Incorrect ZIP information entered. Please enter in the format: ZIP <your-zip-code>", None, None

    zipcode = splits[-1]
    if len(zipcode) != 6:
        return f"Incorrect ZIP code entered ({zipcode}). ZIP code should be 6 numbers, e.g., 422008.", None, zipcode

    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(zipcode)

    return f"Thanks. Your location is {location}", location, zipcode


def craft_response(df, cols_to_disp=['Contact person', 'Contact number', 'Category', 'Source']):
    response = []

    rows = df[cols_to_disp].astype(str).values
    for i in range(len(rows)):
        per_row = '\n'.join(rows[0])
        response.append(per_row)

    response = '\n\n'.join(response)
    return response


def search_location_in_sheet(zipcode, location):
    indices = gsheet['Zip code'] == zipcode

    df = gsheet[indices]
    return craft_response(df)


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
            zip_response, location, zipcode = get_location_from_zip(incoming_msg)

            src_response = search_location_in_sheet(zipcode, location)

            response = zip_response + '\n\n Here is a list of verified resources in your area \n ------- \n\n' + src_response
            msg.body(response)


        return HttpResponse(str(resp))