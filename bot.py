#IMPORTS
import os
import discord
from discord.ext import commands
from table2ascii import table2ascii as t2a, PresetStyle

#load client and environment
client = discord.Client()
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#set commands to start with '!'
bot = commands.Bot(command_prefix='!')

#on ready send confirmation of bot login
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#when a message is sent
@client.event
async def on_message(message):
  #if the command starts with !alliance_chat
  if message.content.startswith('!'):
    await message.channel.send("They treated my nuance like a nuisance")
  
#run bot
client.run(TOKEN)