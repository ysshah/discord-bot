from datetime import datetime, timedelta
from typing import List
import re

import dateparser
from selenium.webdriver.remote.webelement import WebElement

def get_text(elements: List[WebElement]) -> List[str]:
  return [element.text for element in elements]

def parse(time_string: str, date: str) -> datetime:
  trimmed_time = time_string.removeprefix('Scheduled ').removesuffix(' (+1)')
  if re.search(r'\d\d$', trimmed_time):
    trimmed_time += '00'
  time = dateparser.parse(date + ' ' + trimmed_time.replace('IST', '+0530'))
  return time + timedelta(1) if time_string.endswith('(+1)') else time
