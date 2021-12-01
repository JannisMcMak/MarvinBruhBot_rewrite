import discord

import random
import json
from PIL import Image, ImageFont, ImageDraw


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


def get_random_name_combination():
    with open("hidden/name_combinations.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        switcher = data["switcher"]
        endings = data["endings"]
        
        parts = []

        for i in range(1, 5):
            parts.append(switcher.get(str(random.randint(1,4))) + endings[str(i)])

        return " ".join(parts)


def ascii(text, size: int = 15, invert=False):
    """Generate ascii art from Input text

    Parameters
    ----------
    text : str
        Input text
    size : int, optional
        Font size (pt), by default 15
    invert : bool, optional
        Whether the ascii art should be inverted, by default False

    Returns
    -------
    list
        List of rows containing the ascii art
    """

    font = ImageFont.truetype('util/fonts/arialbd.ttf', size)  # load the font
    size = font.getsize(text)  # calc the size of text in pixe

    image = Image.new('1', size, 1)  # create a b/w image
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)  # render the text to the bitmap

    rows = []
    for rownum in range(size[1]):
        line = []
        for colnum in range(size[0]):
            if image.getpixel((colnum, rownum)):
                if invert:
                    line.append('#')
                else:
                    line.append(' ')
            else:
                if invert:
                    line.append(' ')
                else:
                    line.append('#')

        rows.append("".join(line))

    return rows


def get_command_name(message: discord.Message):
    command = message.content.split(" ")
    command = (command[0])[1:]

    return command
