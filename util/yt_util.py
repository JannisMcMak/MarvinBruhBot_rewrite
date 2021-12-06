import discord
import youtube_dl
import asyncio
import json
from youtube_search import YoutubeSearch

from util.logger import Logger

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

log = Logger("YTDL")

class YTDLSource(discord.PCMVolumeTransformer):
    """
    Helper class that handles streaming audio from a Youtube video
    """

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        """Creates a audio player that streams audio from a Youtube video

        Parameters
        ----------
        url : str
            URL of the Youtube video to stream
        loop : asyncio.AbstractEventLoop, optional
            The event loop used to stream the audio. This should be set to the event loop of the discord bot, by default None
        stream : bool, optional
            Whether to stream the audio or download it first, by default False

        Returns
        -------
        discord.FFmpegPCMAudio
            Audio player that streams the Youtube video
        """

        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

    @classmethod
    def search_youtube(cls, search_term):
        """
        Returns Youtube URL of a given search string
        """

        search_result = json.loads(YoutubeSearch(search_term, max_results=5).to_json())
        return search_result["videos"]

    @classmethod
    async def play_in_channel(cls, player, channel):
        """Connects to a voice channel and plays an Mp3 file. Checks if the file and channel exist

        Parameters
        ----------
        player : discord.FFmpegPCMAudio
            Audio player that streams audio. Usually created with :func:`~util.yt_util.YTDLSource.from_url`
        channel : discord.VoiceChannel
            Channel to connect to
        """

        if channel is None:
            log.error("User is not connected to a channel")
            return

        try:
            vc = await channel.connect()
        except:
            log.warn("Skipping... Already connected to a channel")
            return
        
        vc.play(player)
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()