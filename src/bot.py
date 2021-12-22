import os
import discord
import flight

class Bot(discord.Client):

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
      await flight.save_flight_to_calendar(
        message.channel, message.content.removeprefix('$flight '))

Bot().run(os.environ['DISCORD_BOT_TOKEN'])
