# psykikBot.py
# Main code for MiniTibia

from ChatBot.bot import Bot
from Commands.executor import Executor

def main():

    # Start a bot
    bot = Bot("<threadID>", "irc.twitch.tv", 6667, "<login name>", "oauth:<oauthtoken>", "#<channel>")
    # Start executor to execute chat commands
    executor = Executor(bot)

if __name__ == "__main__":
    main()