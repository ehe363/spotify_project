import os
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import json
from IPython.display import Image, display
from pprint import pprint
from dotenv import load_dotenv
from IPython.core.interactiveshell import import_item
import requests
from datetime import datetime, timedelta

load_dotenv() #> invoking this function loads contents of the ".env" file into the script's environment...

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")

#client_id = input("Please enter your SPOTIPY_CLIENT_ID: ")
#client_secret = input("Please enter your SPOTIPY_CLIENT_SECRET: ")
#redirect_uri = input("Please enter Redirect URI:")
# OAuth endpoints given in the Spotify API documentation
# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
# https://developer.spotify.com/documentation/general/guides/authorization/scopes/
scope = ["user-read-currently-playing",
         "user-top-read"]

spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
# Redirect user to Spotify for authorization
authorization_url, state = spotify.authorization_url(authorization_base_url)
print('Please go here and authorize: ', authorization_url)
# Get the authorization verifier code from the callback url
redirect_response = input('\n\nPaste the full redirect URL here: ')

auth = HTTPBasicAuth(client_id, client_secret)
# Fetch the access token
token = spotify.fetch_token(token_url, auth=auth, authorization_response=redirect_response)
print(token)
# Fetch a protected resource, i.e. user profile
r = spotify.get('https://api.spotify.com/v1/me')
print(r.content)


top_artists = spotify.get('https://api.spotify.com/v1/me/top/artists')
top_artists_data = top_artists.content

top_artists_list = json.loads(top_artists_data)['items']
top_artists_names = []
for n in top_artists_list:
    top_artists_names.append(n["name"])

print("Your top artists are:")
for item in top_artists_list:
    print(item["name"])
    display(Image(url=item["images"][0]['url'], height=100))
    print("-----------------------------------------------")

#pprint(top_artists_names)

# Replace 'your_actual_api_key_here' with your real Ticketmaster API key
#os.environ['TICKETMASTER_API_KEY'] = 'iPVCrQgdoj3ZTMll74BfuNig2uiYPZKS'

ticketmaster_api_key = os.getenv('TICKETMASTER_API_KEY')
if ticketmaster_api_key:
    print("Ticketmaster API key is set.")
else:
    print("Ticketmaster API key is not set. Make sure to set it using os.environ.")

# Retrieve API key from environment variable
API_KEY = os.environ.get('TICKETMASTER_API_KEY')
BASE_URL = 'https://app.ticketmaster.com/discovery/v2/'

def search_artist_events(artist_name):
    endpoint = f'{BASE_URL}events.json'
    params = {
        'apikey': API_KEY,
        'keyword': artist_name,
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if response.status_code == 200:
        events = data.get('_embedded', {}).get('events', [])
        return events
    else:
        print('Error:', data.get('detail', 'Unknown error'))
        return None

def filter_events_by_date(events, days):
    today = datetime.now().date()
    end_date = today + timedelta(days=days)

    filtered_events = []
    for event in events:
        event_date = datetime.strptime(event['dates']['start']['localDate'], '%Y-%m-%d').date()
        if today <= event_date < end_date:
            filtered_events.append(event)

    return filtered_events

print("Events matching your top artists:")
for item in top_artists_names:
    events = search_artist_events(item)

    if events:
        filtered_events = filter_events_by_date(events, 90)
        print("-----------------------------------------------------------------------")
        print(f"Found {len(filtered_events)} events for '{item}' in the next 90 days:")
        print("-----------------------------------------------------------------------")
        for event in filtered_events:
            event_name = event['name']
            event_date = event['dates']['start']['localDate']
            event_time = event['dates']['start'].get('localTime', 'Time not available')
            event_url = event.get('url', 'URL not available')

            print(event_name, event_date, event_time)
            print(event_url)
    else:
        print(f"No events found for '{item}'.")
