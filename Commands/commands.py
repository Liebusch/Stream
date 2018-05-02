# commands.py
# Class that holds all possible chat commands

from Crawler import charCrawler
from TibiaObjects.character import Character

class Commands:
    allowed_commands = ['create', 'lookUpCharacter']
    def create (bot, user, attributes):
        vocs = ['Knight', 'Paladin', 'Druid', 'Sorcerer']
        if (attributes[0] in vocs):
            print(attributes[0])
            bot.whisper(user, attributes[
                0] + " created.")

        else:
            bot.whisper(user, attributes[
                0] + " is not recognized as vocation. Please use 'Knight', 'Paladin', 'Druid' or 'Sorcerer'.")

    def lookUpCharacter (bot, user, attributes):
        name = (" ").join(attributes)
        print("Starting")
        char = charCrawler.crawl(name)
        if char:
            bot.whisper(user,
                        "Name: " + char.name +
                        ", Sex: " + char.sex +
                        ", Vocation: " + char.voc +
                        ", Level: " + char.level +
                        ", Achievement Points: " + char.achievement +
                        ", World: " + char.world +
                        ", Residence: " + char.residence +
                        ", Guild Membership: " + char.guild)
        else:
            bot.whisper(user, "Character " + name + " not found. Please check if the name is correct.")
