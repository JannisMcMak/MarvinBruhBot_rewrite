import colorama
from dotenv.main import load_dotenv
from termcolor import colored
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os

colorama.init()
load_dotenv()

class Logger:
    def __init__(self, cog):
        self.name = cog

    def _send(self, message, color):
        print(colored(self._timestamp(), "cyan") + " [" + colored(self.name, "cyan") + "] " + colored(message, color))

    def _timestamp(self):
        now = datetime.now(tz=pytz.timezone(os.environ["TZ"]))
        return now.strftime("%Y-%m-%d-%H:%M:%S")

    def info(self, message):
        self._send(message, "white")

    def warn(self, message):
        self._send(message, "yellow")

    def error(self, message):
        self._send(message, "red")

    def debug(self, message):
        self._send(message, "magenta")

    def success(self, message):
        self._send(message, "green")
