import random
import json
import discord


async def get_gedicht(i):
  with open('hidden/gedichte.json') as json_file:
    data = json.load(json_file)

    if i == 0:
      i = random.randint(1, len(data))
    
    return data.get(str(i), 'Kein Gedicht gefunden...')



def get_command_name(message: discord.Message):
    command = message.content.split(" ")
    command = (command[0])[1:]

    return command
