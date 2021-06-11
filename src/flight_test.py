from datetime import datetime
import unittest
from unittest.mock import AsyncMock, patch

import flight

class FlightTest(unittest.IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.flight = flight.Flight()
    return super().setUp()

  def tearDown(self) -> None:
    self.flight.close()
    return super().tearDown()

  async def test_save_flight_to_calendar(self):
    channel = AsyncMock()
    await self.flight.save_flight_to_calendar(channel, 'UAE533')
    channel.send.assert_called_with('**ERROR:** Expected 2 arguments, got 1')

  @patch('flight.cal')
  async def test_save_flight_to_calendar(self, cal):
    channel = AsyncMock()
    await self.flight.save_flight_to_calendar(channel, 'UAE533 1/4/22')
    cal.insert.assert_called_with(
      datetime.fromisoformat('2022-01-04T04:30:00+05:30'),
      datetime.fromisoformat('2022-01-04T07:05:00+04:00'), 'COK', 'DXB', 'UAE533')

if __name__ == '__main__':
  unittest.main()
