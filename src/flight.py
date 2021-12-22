from datetime import date
import os

from discord import TextChannel
import pytz
import requests

import cal
import util

HEADERS = {'x-apikey': os.environ['AERO_API_KEY']}

def _get_flight(code: str):
  return requests.get(f'https://aeroapi.flightaware.com/aeroapi/flights/{code}', headers=HEADERS)

async def save_flight_to_calendar(channel: TextChannel, message: str):
  args = message.split(' ')
  if len(args) != 2:
    return await channel.send(f'**ERROR:** Expected 2 arguments, got {len(args)}')

  flight_code = args[0]
  departure_date = date.fromisoformat(args[1])
  await channel.send(f'Searching for flight {flight_code}')
  response = _get_flight(flight_code)
  if not response.ok:
    return await channel.send(f'**ERROR:** {response.text}')

  # Documentation here: https://flightaware.com/aeroapi/portal/documentation#get-/flights/-ident-
  info = response.json()['flights'][0]
  flight_code = info['operator_iata'] + info['flight_number']
  src_code, src_tz = util.AIRPORTS[info['origin']['code']].values()
  dst_code, dst_tz = util.AIRPORTS[info['destination']['code']].values()
  departure_time = util.parse(info['scheduled_off'], src_tz)
  arrival_time = util.parse(info['scheduled_on'], dst_tz)
  offset = departure_date - departure_time.date()

  html_link = await cal.insert(
    channel,
    departure_time + offset,
    arrival_time + offset,
    src_code,
    dst_code,
    flight_code)
  await channel.send(f'Created event: {html_link}')
