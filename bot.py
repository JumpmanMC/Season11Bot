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
  #If the message starts with '!winners'
  if message.content.startswith('!add_by_react'):
    command_contents = message.content.split()
    await message.channel.send("Thumbs up this message to join channel: " + command_contents[1])

  #if the command starts with !alliance_chat
  if message.content.startswith('!alliance_chat'):
    # creates array [!alliance_chat, input_1, input_2...]
    command_contents = message.content.split()
    #throw error if fewer than 3 inputs
    if len(command_contents) < 3:
      await message.channel.send('Alliance chats need at least two players!')
    else: 
      #remove '!alliance_chat' from array of names
      command_contents.pop(0)
      #keep the channel secret by default
      overwrites = {
        message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        message.guild.me: discord.PermissionOverwrite(read_messages=True)
      }
      #loops through inputs and create string in form 'name-' while opening channel to roles
      names = ''
      name_dupes = []
      duplicates = False
      for name in command_contents:
        #checks for duplicate names
        for dup_name in name_dupes:
          if name == dup_name:
            duplicates = True
            await message.channel.send('Alliance chat cannot be created because there are duplicate names!')
        name_dupes.append(name)
        #find the role associated with the player name
        role = discord.utils.get(message.guild.roles, name=name)
        #opens the channel to the player
        overwrites[role] = discord.PermissionOverwrite(read_messages=True)
        names = names + name + '-'
      #remove the last '-'
      chat_name = names[:-1]
  
      #find the host role
      host = discord.utils.get(message.guild.roles, name="Host")
      #open the channel to the host
      overwrites[host] = discord.PermissionOverwrite(read_messages=True)
  
      #finds members with the head of logistics role
      hol = discord.utils.get(message.guild.roles, name="Head of Logistics")
      #open the channel to head of logistics
      overwrites[hol] = discord.PermissionOverwrite(read_messages=True)

      #finds members with the head of filming role
      hof = discord.utils.get(message.guild.roles, name="Head of Filming")
      #open the channel to head of filming
      overwrites[hof] = discord.PermissionOverwrite(read_messages=True)
      
      #Finds the 'Alliance Chats' category 
      category = discord.utils.get(message.guild.categories, name="Alliance Chats")
      
      #If there were no duplicate names
      if duplicates == False:
        #create channel with assembled name, overwrites and category
        try:
          await message.guild.create_text_channel(chat_name, overwrites=overwrites, category=category)
          await message.channel.send('Chat ' + chat_name + ' created!')
        #error if it fails
        except:
          await message.channel.send('Error creating chat! Make sure player names are spelled correctly!')

  #If the message starts with '!commands'
  if message.content.startswith('!commands'):
    #Output the new amsterdam message.
    await message.channel.send("alliance_chat\ncommands\ndevs\nhelp\nhosts\nnew_amsterdam\nrequest_filmer\nwinners")

  #if the command starts with !create_open_channel
  if message.content.startswith('!create_channel'):
    command_contents = message.content.split()
    #throw error if fewer than 2 inputs
    if len(command_contents) < 2:
      await message.channel.send('Channel name needed!')
    else:
      overwrites = {
        message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        message.guild.me: discord.PermissionOverwrite(read_messages=True)
      }
      #finds members with the head of logistics role
      hol = discord.utils.get(message.guild.roles, name="Head of Logistics")
      #open the channel to head of logistics
      overwrites[hol] = discord.PermissionOverwrite(read_messages=True)

      #finds members with the head of logistics role
      botm = discord.utils.get(message.guild.roles, name="BotMaster")
      #open the channel to head of logistics
      overwrites[botm] = discord.PermissionOverwrite(read_messages=True)

      category = discord.utils.get(message.guild.categories, name="FUN CHANNELS")
      eboard = discord.utils.get(message.guild.roles, name="Eboard")
      botmaster = discord.utils.get(message.guild.roles, name="BotMaster")
      if ((eboard in message.author.roles) | (botmaster in message.author.roles)):
        await message.guild.create_text_channel(command_contents[1], overwrites=overwrites, category=category)
        await message.channel.send('Channel ' + command_contents[1] + " created!")
      else:
        await message.channel.send("You do not have permission stinky!!!!")
  #If the message starts with '!devs'
  if message.content.startswith('!devs'):
    #Output the new amsterdam message.
    await message.channel.send("This bot was developed by Harrison Jumper with additional programming by Juliana Sica")
  
  #If the message starts with '!help'
  if message.content.startswith('!help'):
    #send the documentation
    await message.channel.send("https://docs.google.com/document/d/1mRM8xl5f2_zhOgsapYVhOHUXql13RGacO_wCArEuyuU/edit?usp=sharing")
  
  #If the message starts with '!hosts'
  if message.content.startswith('!hosts'):
    #Create the output table of hosts.
    print("hosts")
    output = t2a(
      header=["Seasons", "Host"],
      body=[['11-12', 'Payton McAlice'],
            ['9-10', 'Lauren Murphy'],
            ['7-8', 'Andy Lok'], 
            ['6-7', 'Andrew Carlson'],
            ['4-5', 'Rob Mennuti'],
            ['1-3', 'Casey Abel'],],
      style=PresetStyle.thin_compact,
      first_col_heading=True
    )
    #send host table
    await message.channel.send(f"```\n{output}\n```")

  #If the message starts with '!new_amsterdam'
  if message.content.startswith('!new_amsterdam'):
    #Output the new amsterdam message.
    with open('new_amsterdam.txt') as f:
      text = f.read()
      await message.channel.send(text)

  #If the message starts with '!request_filmer'
  if message.content.startswith('!request_filmer'):
    #store id of the filming chanel
    id = 972228042686615663
    #get the filming channel
    channel = client.get_channel(id)
    #get array of command contents
    command_contents = message.content.split()
    #throw error if fewer than 2 inputs
    if len(command_contents) < 2:
      await message.channel.send('Description of what will be filmed and when is needed!')
    #get prod role
    prod = discord.utils.get(message.guild.roles, name="Prod")
    #sends the filming request to the filming channel
    await channel.send("Filmer requested: " + message.content[15:] + " (::" + message.channel.name + ") " + prod.mention)

  #If the message starts with '!winners'
  if message.content.startswith('!winners'):
    #Create the output table of winners.
    print("winners")
    output = t2a(
      header=["Season", "Winner"],
      body=[[10, 'Margaret Morehead'],
            [9, 'Katalina Baehring'],
            [8, 'Stephanie Yee'], 
            [7, 'Lauren Murphy'],
            [6, 'Delanie Smither'],
            [5, 'Alexander Sharp'],
            [4, 'James Zemartis'],
            [3, 'Austin Shaughnessy'],
            [2, 'Lydia Tavera'],
            [1, 'Ryan Mallaby']],
      style=PresetStyle.thin_compact,
      first_col_heading=True
    )
    #send winners table
    await message.channel.send(f"```\n{output}\n```")

@client.event
async def on_reaction_add(reaction, user):
    if user != client.user:
        #if a message is given a thumbs up reaction
        if str(reaction.emoji) == "👍":
          #if the message is a filming request and this is the first reaction
           if((reaction.message.content[:17] == 'Filmer requested:') & (reaction.count < 2)):
            #parse out the chat it was sent from
            chat_name = reaction.message.content.split('(::')[1].split(')')[0]
            #find the corresponding channel
            channel = discord.utils.get(client.get_all_channels(), name=chat_name)
            #pull the channel id
            id = channel.id
            #get channel object
            channel = client.get_channel(id)
            #get prod role
            prod = discord.utils.get(reaction.message.guild.roles, name="Prod")
            #if a prod member liked the message
            if prod in user.roles:
              #pull the channel id
              filming_id = 1028066374448328804
              #get channel object
              filming_channel = client.get_channel(filming_id)
              #send who is filming meeting to filming_messages channel
              await filming_channel.send(str(user.display_name) + " is filming the requested meeting: " + reaction.message.content[17:].split('(')[0])
              #add the user to chanel and send filmer confirmation
              await channel.set_permissions(user, read_messages=True)
              await channel.send(str(user.display_name) + " is filming the requested meeting: " + reaction.message.content[17:].split('(')[0])
           if(reaction.message.content[:39] == 'Thumbs up this message to join channel:'):
                chat_name = reaction.message.content.split(': ')[1]
                channel = discord.utils.get(client.get_all_channels(), name=chat_name)
                await channel.set_permissions(user, read_messages=True)
  
#run bot
client.run(TOKEN)