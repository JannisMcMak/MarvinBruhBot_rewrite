import colorama
from dotenv.main import load_dotenv
from termcolor import colored
from datetime import datetime
import pytz
import config

colorama.init()

class Logger:
    """
    Handles logging
    """

    def __init__(self, name):
        """Creates logger object

        Parameters
        ----------
        name : str
            Name of the logging instance that shows up in the log (Usually the name of the cog/module)
        """

        self.name = name

    def __send(self, message, color):
        now = datetime.now(tz=pytz.timezone(config.TZ))
        timestamp = now.strftime("%Y-%m-%d-%H:%M:%S")
        print(colored(timestamp, "cyan") +
              " [" + colored(self.name, "cyan") + "] " + colored(message, color))

    def info(self, message):
        """Sends log message with level INFO (white)

        Parameters
        ----------
        message : str
            Message to send
        """

        self.__send(message, "white")

    def warn(self, message):
        """Sends log message with level WARN (yellow)

        Parameters
        ----------
        message : str
            Message to send
        """

        self.__send(message, "yellow")

    def error(self, message):
        """Sends log message with level ERROR (red)

        Parameters
        ----------
        message : str
            Message to send
        """

        self.__send(message, "red")

    def debug(self, message):
        """Sends log message with level DEBUG (magenta)

        Parameters
        ----------
        message : str
            Message to send
        """

        self.__send(message, "magenta")

    def success(self, message):
        """Sends log message with level SUCCESS (green)

        Parameters
        ----------
        message : str
            Message to send
        """

        self.__send(message, "green")
