import random
import json
import discord


async def get_gedicht(i):
  with open('hidden/gedichte.json') as json_file:
    data = json.load(json_file)

    if i == 0:
      i = random.randint(1, len(data))
    
    return data.get(str(i), 'Kein Gedicht gefunden...')

async def get_time_notification(i):
  with open('hidden/time_notifications.json') as json_file:
    data = json.load(json_file)

    if i == 0:
      i = random.randint(1, len(data))
    
    return data.get(str(i), "I don't no man")

async def get_bitch_voiceline(i):
  with open('hidden/bitch_voicelines.json') as json_file:
    data = json.load(json_file)
    
    return data.get(str(i), "{} is a little bitch")



def get_command_name(message: discord.Message):
    command = message.content.split(" ")
    command = (command[0])[1:]

    return command
