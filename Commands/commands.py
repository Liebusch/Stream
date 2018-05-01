# commands.py
# Class that holds all possible chat commands


class Commands:
    allowed_commands = ['create']
    def create (bot, user, attributes):
        vocs = ['Knight', 'Paladin', 'Druid', 'Sorcerer']
        if (attributes[0] in vocs):
            print(attributes[0])
            bot.whisper(user, attributes[
                0] + " created.")

        else:
            bot.whisper(user, attributes[
                0] + " is not recognized as vocation. Please use 'Knight', 'Paladin', 'Druid' or 'Sorcerer'.")
