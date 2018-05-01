# psykikBot.py
# Main code for MiniTibia

from ChatBot.bot import Bot
from Commands.executor import Executor


def main():

    # Start a bot
    bot = Bot("bot1", "irc.twitch.tv", 6667, "GameMusicBot", "oauth:wh9ppddv9kej8y5gkm4kf3dqvdgy00", "#hasorko")
    # Start executor to execute chat commands
    executor = Executor(bot)


if __name__ == "__main__":
    main()