import colorama
from termcolor import colored
from datetime import datetime

colorama.init()

class Logger:
    def __init__(self, cog):
        self.name = cog

    def _send(self, message, color):
        print(colored(self._timestamp(), "blue") + " [" + colored(self.name, "cyan") + "] " + colored(message, color))

    def _timestamp(self):
        now = datetime.now()
        return now.strftime("%Y-%m-%d-%H:%M:%S")

    def info(self, message):
        self._send(message, "white")

    def warn(self, message):
        self._send(message, "yellow")

    def error(self, message):
        self._send(message, "red")

    def debug(self, message):
        self._send(message, "grey")

    def success(self, message):
        self._send(message, "green")
