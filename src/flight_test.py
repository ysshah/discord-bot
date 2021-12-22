from datetime import datetime
import unittest
from unittest.mock import AsyncMock, Mock, patch

import flight

class FlightTest(unittest.IsolatedAsyncioTestCase):

  async def test_save_flight_to_calendar(self):
    channel = AsyncMock()
    await flight.save_flight_to_calendar(channel, 'UAE533')
    channel.send.assert_called_with('**ERROR:** Expected 2 arguments, got 1')

  @patch('flight.cal', new_callable=AsyncMock)
  @patch('flight.requests')
  async def test_save_flight_to_calendar(self, requests, cal):
    channel = AsyncMock()
    requests.get.return_value.json.return_value = {
      'flights': [{
        'operator_iata': 'EK',
        'flight_number': '533',
        'origin': {'code': 'VOCI'},
        'destination': {'code': 'OMDB'},
        'scheduled_off': '2021-12-23T23:00:00Z',
        'scheduled_on': '2021-12-24T03:05:00Z',
      }]
    }

    await flight.save_flight_to_calendar(channel, 'UAE533 2022-01-04')

    cal.insert.assert_called_with(
      channel,
      datetime.fromisoformat('2022-01-04T04:30:00+05:30'),
      datetime.fromisoformat('2022-01-04T07:05:00+04:00'), 'COK', 'DXB', 'EK533')

if __name__ == '__main__':
  unittest.main()
