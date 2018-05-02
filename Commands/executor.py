# executor.py
# Executes commands from chat.

from Commands.commands import Commands as commands
from threading import Thread
from time import sleep

class Executor:

    def __init__(self, bot):
        # Function: execute
        # Run function of thread to work through each message.
        #   Parameters:
        #       bot -- corresponding bot instance to message the user
        def execute(bot):
            while True:
                try:
                    message = bot.messages.popleft()
                    if (message.message[0]=="!"):
                        self.executeCommand(message,bot)
                except IndexError as e:
                    'Do Nothing'
            sleep(1.5)

        t1 = Thread(target=execute(bot), args=(self,))
        t1.start()

    # Function: executeCommand
    # Main control unit of bot. Executes defined
    # commands, which were found in chat.
    #   Parameters:
    #       user -- who send the message
    #       command -- defines which function is being run
    #       attributes -- list of attributes for the function
    #       bot -- corresponding bot instance to message the user

    def executeCommand (self, message, bot):
        command = ""
        index = message.message.find(' ')
        if (index>-1):
            command = message.message[1:index]
            attributes = message.message[index:].split()
        if (command in commands.allowed_commands):
            # function corresponding to command
            fn = getattr(commands, command, None)
            if callable(fn):
                t1 = Thread(target=fn(bot, message.user, attributes), args=(self,))
                t1.start()
            else:
                print("ERROR: Couldn't find corresponding function to command \"" + command + "\".")
        else:
            bot.whisper(message.user,"Command \"" + command + "\" unkown. Type !instructions for help.")