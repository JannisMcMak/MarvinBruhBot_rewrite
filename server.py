from quart import Quart, render_template, request, redirect, flash, session
import os, shutil
import json
import main
import asyncio
from replit import db
from quart_cors import cors

app = Quart('Keep alive')
app.config["UPLOAD_FOLDER"] = './mp3s'
#app.config['UPLOADED_FILES_ALLOW'] = ["MP3"]
app.config["SECRET_KEY"] = "marvinbruhbot123asdf"
app.config['CORS_HEADERS'] = 'Content-Type'
cors(app)

@app.route('/')
async def home():
  counters, values = await main.get_counters()

  for counter, value in zip(counters, values):
    db[counter] = value

  clear_cache()
  return "Hello"


@app.route('/gedichte', methods=['GET', 'POST'])
async def add_gedicht():
  if request.method == 'POST':
    gedicht = (await request.form)['name']
    print('Neues Gedicht:', gedicht)

    with open('gedichte.json') as json_file:
      data = json.load(json_file)
      
      data[str(len(data)+1)] = gedicht

    with open('gedichte.json', 'w') as out:
      json.dump(data, out)
      

  return await render_template('gedichte.html')


@app.route('/mp3s', methods=['GET', 'POST'])
async def add_mp3():
  if request.method == 'POST':
    name = (await request.form)['name']
    filename = name.lower() + '.mp3'
    dir = 'mp3s/' + filename

    f = (await request.files)['file']
    f.save(dir)

    print(filename)
  
  return await render_template('mp3.html')


async def run():
  await app.run_task(host='0.0.0.0', port=8080)
  clear_cache()


def clear_cache():
  print('Clearing cache...')
  folder = 'cache'
  for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
      if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
      elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
    except Exception as e:
      print('Error clearing cache: {}'.format(e))


