# character.py
# Stores data of a character in Tibia.

class Character:
    def __init__(self, name, level="", world="", voc="", sex="", achievement="", residence="", guild=""):
        self.name = name
        self.level = level
        self.world = world
        self.voc = voc
        self.sex = sex
        self.achievement = achievement
        self.residence = residence
        self.guild = guild
