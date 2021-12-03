import discord
from ibm_cloud_sdk_core import authenticators

import requests
import json
import time
import asyncio
import os.path
import config
import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from util.logger import Logger

log = Logger("TTS-Handler")


async def play_in_channel(filename, channel):
    """Connects to a voice channel and plays an Mp3 file. Checks if the file and channel exist  

    Parameters
    ----------
    filename : str
        Path to the Mp3 file to play
    channel : discord.VoiceChannel
        Channel to connect to
    """

    if not os.path.isfile(filename):
        log.error("Mp3 file does not exist.")
        return

    if channel is None:
        log.error("User is not connected to a channel")
        return

    vc = None

    try:
        vc = await channel.connect()
    except:
        log.warn("Skipping... Already connected to a channel")
        return

    vc.play(discord.FFmpegPCMAudio(source=filename))

    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()


async def write_mp3(text, lang: str = "de", formatted: bool = False):
    """Uses an API to write an Mp3 file to a temporary folder containing a TTS message

    Parameters
    ----------
    text : str or list[str]
        The text to convert to TTS
    lang : str, optional
        The language of the TTS message. Allowed are "eng", "ind" and "de", by default "de"
    formatted : bool, optional
        Whether the text is already a string. Set to False if the text is passed as a list of strings. By default False

    Returns
    -------
    str
        Path to the Mp3 file containing the TTS message
    """

    if not formatted:
        text = ' '.join(text)
    log.info(text)

    if lang == "eng":
        url = 'http://api.voicerss.org/?key=16d017cd4d194a22b199c5739bd6ab42&hl=en-us&v=Mike&src={}'
    elif lang == "ind":
        url = 'http://api.voicerss.org/?key=16d017cd4d194a22b199c5739bd6ab42&hl=en-in&v=Ajit&src={}'
    else:
        url = 'http://api.voicerss.org/?key=16d017cd4d194a22b199c5739bd6ab42&hl=de-de&v=Jonas&src={}'

    r = requests.get(url.format(text))

    filename = 'cache/{}.mp3'.format(time.time())
    open(filename, 'wb').write(r.content)

    return filename

async def write_mp3_ibm(text, lang: str = "de", formatted: bool = False):
    """Uses an API to write an Mp3 file to a temporary folder containing a TTS message

    Parameters
    ----------
    text : str or list[str]
        The text to convert to TTS
    lang : str, optional
        The language of the TTS message. Allowed are "p"
    formatted : bool, optional
        Whether the text is already a string. Set to False if the text is passed as a list of strings. By default False

    Returns
    -------
    str
        Path to the Mp3 file containing the TTS message
    """

    if not formatted:
        text = ' '.join(text)
    log.info(text)

    authenticator = IAMAuthenticator(f'{config.IBM_TTS_API_KEY}')
    ibm_tts = TextToSpeechV1(authenticator=authenticator)
    ibm_tts.set_service_url(f'{config.IBM_TTS_API_URL}')
    
    voice = ""
    if lang == "p":
        voice = "de-DE_BirgitV3Voice"
       

    filename = 'cache/{}.mp3'.format(time.time())
    
    with open(filename, 'wb') as audio_file:
        audio_file.write(ibm_tts.synthesize(
            text,
            voice=voice,
            accept='audio/mp3'
        ).get_result().content)

    return filename


async def write_mp3_twitch(text, formatted: bool = False):
    """Uses an API to write an Mp3 file to a temporary folder containing a TTS message with Brian's voice (from Twitch donation messages)

    Parameters
    ----------
    text : str or list[str]
        The text to convert to TTS
    formatted : bool, optional
        Whether the text is already a string. Set to False if the text is passed as a list of strings. By default False

    Returns
    -------
    str
        Path to the Mp3 file containing the TTS message
    """

    if not formatted:
        text = ' '.join(text)
    log.info(text)

    if len(text.encode('utf-8')) >= 550:
        return None

    base_url = config.TWITCH_TTS_API_URL
    data = {"voice": "Brian", "text": text}

    r = requests.post(base_url.format(text), data)
    j = json.loads(r.text)
    url = j["speak_url"]
    r = requests.get(url)

    filename = 'cache/{}.mp3'.format(time.time())
    open(filename, 'wb').write(r.content)

    return filename
