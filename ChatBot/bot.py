# ChatBot.py
# Class to create a Twitch ChatBot

import socket
import re
from threading import Thread
import json
from urllib import request
import urllib.error
from time import sleep
from Database.connection import Connection
from collections import deque
from Messages.message import Message

class Bot:
    def __init__(self, threadID, host, port, nick, passw, chan):
        self.threadID = threadID
        self.host = host
        self.port = port
        self.nick = nick
        self.passw = passw
        self.chan = chan
        self.messages = deque()

        # Networking functions
        # Connects to corresponding Twitch Chat
        self.s = socket.socket()
        self.s.connect((self.host, self.port))
        self.s.sendall("PASS {}\r\n".format(self.passw).encode("utf-8"))
        self.s.sendall("NICK {}\r\n".format(self.nick).encode("utf-8"))
        self.s.sendall("JOIN {}\r\n".format(self.chan).encode("utf-8"))
        self.s.sendall(("CAP REQ :twitch.tv/commands\n").encode("utf-8"))

        # Function: collectMesages
        # Collects all messages in twitch chat
        def collectMesages(self):
            # Parses messages to a more readable format
            CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
            CHAT_WHSP = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv WHISPER \w+ :")
            while True:
                try:
                    # Grab recent messages
                    response = self.s.recv(4096).decode("utf-8")
                    # Split response in list of messages
                    messageList = response.splitlines()
                except socket.error as e:
                    print(e)
                for line in messageList:
                    # Check if message was ping, bot has to reply to not get disconnected
                    if line == "PING :tmi.twitch.tv\r\n":
                        self.s.sendall("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                    else:
                        # Extract username who send message
                        username = re.search(r"\w+", line).group(0)
                        # Extract message; distinguishes between chat and whisper
                        message = line
                        if "WHISPER" in line:
                            message = Message(username,CHAT_WHSP.sub("", line),"whisper")
                            self.messages.append(message)
                        if "PRIVMSG" in line:
                            message = Message(username,CHAT_MSG.sub("", line),"chat")
                            self.messages.append(message)
                # Delay between gathering messages
                sleep(1.5)
        # Thread to keep checking for new messages
        t1 = Thread(target=collectMesages, args=(self,))
        t1.start()

        # Function: registerViewers
        # Regularly checks viewers and saves them
        def registerViewers(self):
            # database connection to save new viewers
            db = Connection("ViewerData.db")
            while True:
                # Connection to Twitch viewer API
                url = "http://tmi.twitch.tv/group/user/" + (self.chan).replace("#","") + "/chatters"
                req = request.Request(url, headers={"accept": "*/*"})
                try:
                    response = request.urlopen(req).read()
                    if response.find("502 Bad Gateway".encode("utf-8")) == -1:
                        data = json.loads(response)
                        # Goes through each user in each role and checks,
                        # if user is already in database. If not he is added.
                        for role in data["chatters"]:
                            for p in data["chatters"][role]:
                                db.cur.execute("SELECT count(1) FROM Viewer WHERE Name ='" + p + "'")
                                viewerExists = db.cur.fetchone()[0]
                                if (viewerExists==0):
                                    print("Im adding.")
                                    db.cur.execute("INSERT INTO Viewer VALUES(null, '" + p + "','" + role + "')")
                                    db.con.commit()
                except urllib.error.HTTPError as e:
                    print(e)
            # Delay between checking for viewers
            sleep(60)

        # Thread to keep checking for new viewers
        t2 = Thread(target=registerViewers, args=(self,))
        t2.start()



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