from app import search_artist_events, filter_events_by_date
from datetime import datetime, timedelta
import json
import os

today = datetime.now().date()

def test_data_fetching():
    result = search_artist_events("Drake")
    result_filtered = filter_events_by_date(result, 90)
    for event in result_filtered:
        event_date = event['dates']['start']['localDate']
        assert datetime.strptime(event_date,'%y-%m-%d') > today
