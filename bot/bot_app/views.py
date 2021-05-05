from os.path import splitext

from geopy.geocoders import Nominatim

from django.shortcuts import render

# Create your views here.
from twilio.twiml.messaging_response import MessagingResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# import sys
# sys.path.append('/Users/piyushbagad/personal/projects/covid-whatsapp-bot/')

from data.gsheets import get_gsheet
from utils.pandas import apply_filters

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

    if len(rows) == 0:
        return "Sorry. No resource found."

    for i in range(len(rows)):
        values = []
        for j, value in enumerate(rows[i]):
            value = f'*{cols_to_disp[j]}*: {value}'
            values.append(value)

        per_row = '\n'.join(values)
        response.append(per_row)

    response = '\n\n'.join(response)
    return response


def search_location_in_sheet(zipcode, location):
    indices = gsheet['Zip code'] == zipcode

    df = gsheet[indices]
    return craft_response(df)


def _check_valid_entry(entry, attribute):
    splits = entry.split(':')
    splits = [x.replace(' ', '') for x in splits]

    def_resp = f"Information entered incorrectly. \
        Please enter in the format: '{attribute}: <your-entry>'"
    def_entry_input = None
    if splits[0] != attribute:
        resp = def_resp
        entry_input = def_entry_input
    
    if len(splits) >= 2:
        entry_input = ' '.join(splits[1:])
        resp = f"You chose {attribute} as {entry_input}"
    else:
        resp = def_resp
        entry_input = def_entry_input
    
    return resp, entry_input


def get_response_for_help(incoming_msg):
    lines = incoming_msg.split('\n')[1:]
    city = ' '.join(lines[0].split(': ')[1:])
    resource = ' '.join(lines[1].split(': ')[1:])
    filters = {'City': city.lower(), 'Category': resource.lower()}
    df = gsheet.apply(lambda x: x.astype(str).str.lower())
    df = apply_filters(df, filters)
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
            response = "*Hi! Thanks for contacting COVID Helper Bot*.\n\n"\
                "Please enter city and requirement in following format to get help:\n"\
                "Help\n"\
                "City: Mumbai\n"\
                "Req: Oxygen\n\n"\
                "Resources in your city shall be displayed. Thanks for being patient.'\n"

            msg.body(response)

        elif incoming_msg.startswith('zip'):
            zip_response, location, zipcode = get_location_from_zip(incoming_msg)

            src_response = search_location_in_sheet(zipcode, location)

            breaker = '\n\n Here is a list of verified resources in your area \n ------- \n\n'
            response = zip_response + breaker  + src_response
            msg.body(response)

        elif incoming_msg.startswith('city'):
            response, entry_input = _check_valid_entry(entry, attribute='city')

            if entry_input:
                df = apply_filters(gsheet, {'City': entry_input})
        
        elif incoming_msg.startswith('help'):
            response = get_response_for_help(incoming_msg)
            msg.body(response)

        else:
            response = "Incorrect information supplied. Please enter city and requirement in following format to get help: \n"\
                "Help\n"\
                "City: Mumbai\n"\
                "Req: Oxygen\n\n"\
                "Resources in your city shall be displayed. Thanks for being patient.'\n"
            msg.body(response)

        return HttpResponse(str(resp))