import random
import itertools
import json

#-----------------------------Text generators--------------------------------------------
async def get_gedicht(i):
  with open('gedichte.json') as json_file:
    data = json.load(json_file)
    print(len(data))
    if i == 0:
      i = random.randint(1, len(data))
    
    print(i)

    return data.get(str(i), 'Kein Gedicht gefunden...')



#-----------------------------Simon Name Generator--------------------------------------------
