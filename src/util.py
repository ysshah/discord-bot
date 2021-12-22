from datetime import datetime
import json
from os.path import dirname, join, realpath
from pytz import timezone

AIRPORTS = {}
with open(join(dirname(realpath(__file__)), 'airports.json'), 'r') as fp:
  AIRPORTS = json.load(fp)

def parse(time_string: str, src_tz: str) -> datetime:
  return datetime.fromisoformat(time_string.replace('Z', '+00:00')).astimezone(timezone(src_tz))

def _convert_airports_csv_to_json():
  '''
  Converts airports.csv from:
  https://raw.githubusercontent.com/mborsetti/airportsdata/main/airportsdata/airports.csv
  '''
  import pandas as pd
  df = pd.read_csv('airports.csv')
  with open('airports.json', 'w') as f:
    df.dropna()[['icao', 'iata', 'tz']].set_index('icao').to_json(f, orient='index')
