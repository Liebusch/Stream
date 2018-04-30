# MiniTibia.py
# Main code for MiniTibia

import Bot


def main():
    print("Initialize Bot")
    bot = Bot.Bot("bot1", "irc.twitch.tv", 6667, "GameMusicBot", "oauth:wh9ppddv9kej8y5gkm4kf3dqvdgy00", "#hasorko")
    print("Bot Initialized")
    bot.start()
    bot.chat("I'm running.")

if __name__ == "__main__":
    main()