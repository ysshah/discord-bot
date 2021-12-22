from datetime import datetime
from discord import TextChannel
import json
import os

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

credentials = Credentials.from_service_account_info(json.loads(os.environ['SERVICE_ACCOUNT_JSON']))
service = build('calendar', 'v3', credentials=credentials)

def _format(time: datetime) -> str:
  return time.strftime('%a %b %d at %I:%M %p')

async def insert(channel: TextChannel, start: datetime, end: datetime, src: str, dst: str, flight_code: str) -> str:
  '''Inserts a flight into the calendar and returns a link to the created event.'''
  body = {
    'summary': f'{src} -> {dst} ({flight_code})',
    'description': f'Departing {src} on {_format(start)}\nArriving at {dst} on {_format(end)}',
    'start': { 'dateTime': start.isoformat(), 'timeZone': start.tzinfo.zone },
    'end': { 'dateTime': end.isoformat(), 'timeZone': end.tzinfo.zone },
  }
  await channel.send(f'Creating event with body {body}')
  event = service.events().insert(calendarId='yashshah0127@gmail.com', body=body).execute()
  return event['htmlLink']
