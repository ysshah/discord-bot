import os
import discord
from flight import Flight

class Bot(discord.Client):
  def __init__(self, *, loop=None, **options):
    super().__init__(loop=loop, **options)
    self.flight = Flight()

  async def on_ready(self):
    print('Logged in')

  async def on_message(self, message: discord.Message):
    '''
    Docs for `message`: https://discordpy.readthedocs.io/en/latest/api.html#discord.Message
    '''
    # Ignore messages sent by the bot
    if message.author.id == self.user.id:
      return
    if message.content.startswith('$flight '):
      await self.flight.save_flight_to_calendar(
        message.channel, message.content.removeprefix('$flight '))

  async def close(self):
    print('Closing')
    self.flight.close()
    await super().close()

Bot().run(os.environ['DISCORD_BOT_TOKEN'])
