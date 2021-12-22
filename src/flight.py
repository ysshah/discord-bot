import os

from discord import TextChannel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import cal
import util

OPTIONS = Options()
OPTIONS.headless = True
OPTIONS.add_argument('--disable-gpu')
OPTIONS.add_argument('--no-sandbox')

class Flight:

  async def save_flight_to_calendar(self, channel: TextChannel, message: str):
    args = message.split(' ')
    if len(args) != 2:
      await channel.send(f'**ERROR:** Expected 2 arguments, got {len(args)}')
      return
    flight_code, date = args
    await channel.send(f'Searching for flight {flight_code}')
    browser = webdriver.Chrome(service=Service(os.environ['CHROMEDRIVER_PATH']), options=OPTIONS)
    browser.get(f'https://flightaware.com/live/flight/{flight_code}')
    texts = util.get_text(browser.find_elements(By.CLASS_NAME, 'flightPageDataAncillaryText'))
    departure_time = util.parse(texts[0], date)
    arrival_time = util.parse(texts[5], date)
    src_airport_code, dst_airport_code, _ = util.get_text(
      browser
        .find_element(By.ID, 'flightPageTourStep1')
        .find_elements(By.CLASS_NAME, 'displayFlexElementContainer'))
    browser.quit()
    await channel.send(f'Creating event for flight from {src_airport_code} at {departure_time} to {dst_airport_code} at {arrival_time}')
    html_link = cal.insert(departure_time, arrival_time, src_airport_code, dst_airport_code, flight_code)
    await channel.send(f'Created event: {html_link}')
