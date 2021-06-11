from datetime import datetime
import json
import os

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

credentials = Credentials.from_service_account_info(json.loads(os.environ['SERVICE_ACCOUNT_JSON']))
service = build('calendar', 'v3', credentials=credentials)

def _format(time: datetime) -> str:
  return time.strftime('%a %b %d at %I:%M %p')

def insert(start: datetime, end: datetime, src: str, dst: str, flight_code: str) -> str:
  '''Inserts a flight into the calendar and returns a link to the created event.'''
  event = service.events().insert(calendarId='yashshah0127@gmail.com', body={
    'summary': f'{src} -> {dst} ({flight_code})',
    'description': f'Departing {src} on {_format(start)}\nArriving at {dst} on {_format(end)}',
    'start': { 'dateTime': start.isoformat() },
    'end': { 'dateTime': end.isoformat() },
  }).execute()
  return event['htmlLink']
