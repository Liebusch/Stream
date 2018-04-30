# ChatBot.py
# Class to create a Twitch ChatBot

import socket
import re
import threading
from time import sleep


class Bot(threading.Thread):
    def __init__(self, threadID, host, port, nick, passw, chan):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.host = host
        self.port = port
        self.nick = nick
        self.passw = passw
        self.chan = chan

        # Networking functions
        # Connects to corresponding Twitch Chat
        self.s = socket.socket()
        self.s.connect((self.host, self.port))
        self.s.sendall("PASS {}\r\n".format(self.passw).encode("utf-8"))
        self.s.sendall("NICK {}\r\n".format(self.nick).encode("utf-8"))
        self.s.sendall("JOIN {}\r\n".format(self.chan).encode("utf-8"))
        self.s.sendall(("CAP REQ :twitch.tv/commands\n").encode("utf-8"))



    # Function: run
    # Listens to all messages in twitch chat
    def run(self):
        CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        CHAT_WHSP = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv WHISPER \w+ :")
        while True:
            try:
                response = self.s.recv(1024).decode("utf-8")
                messageList = response.splitlines()
            except socket.error as e:
                print(e)
            for line in messageList:
                if line == "PING :tmi.twitch.tv\r\n":
                    self.s.sendall("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                else:
                    username = re.search(r"\w+", line).group(0)  # return the entire match
                    message = line
                    if "WHISPER" in line:
                        message = "whispers: " + CHAT_WHSP.sub("", line)
                    if "PRIVMSG" in line:
                        message = "says: " + CHAT_MSG.sub("", line)
                    print(username + " " + message)

            sleep(1.5)

    # Function: chat
    # Send a chat message to the server.
    #   Parameters:
    #       msg -- the message to send
    def chat(self, msg):
        self.s.sendall("PRIVMSG {} :{}\r\n".format(self.chan, msg).encode('utf-8'))

    # Function: whisper
    # Send a whisper message to a user.
    #   Parameters:
    #       user -- the user to message
    #       msg -- the message to send
    def whisper(self, user, msg):
        messageTemp = "PRIVMSG #jtv :.w " + user + " " + msg
        self.s.sendall((messageTemp + "\r\n").encode('utf-8'))
        print("Sent whisper: " + messageTemp)