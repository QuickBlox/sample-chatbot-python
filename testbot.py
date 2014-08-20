#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    TestBot: a QuickBlox compatible chat bot.
    This is a basic chat bot code that works in both 1:1 and MUC chat environments.
    Can be used for adding automated agents into QuickBlox powered apps. Typical use cases include testing, moderation, customer support, trivia/quiz games etc.
    All custom and QuickBlox related code copyright (C) 2014 Taras Filatov and QuickBlox.
    Based on the code from SleekXMPP project by Nathanael C. Fritz. (C) 2010.
    Distributed under Apache 2.0 open source license. See the file LICENSE for copying permission including bundled 3rd party codes.
"""

import sys
import logging
import getpass
import os
from optparse import OptionParser
import sleekxmpp
import subprocess

"""
   IMPORTANT: for MUC auto-join to work, change these to your own script path and QuickBlox credentials.
   Also make sure you made this script executable (chmod -x testbot.py).
"""

selfPath = os.path.realpath(__file__)
qbAppID = "7232"
qbUserID = "1265350"
qbUserPass = "niichavo"
qbChatLogin = qbUserID + "-" + qbAppID + "@chat.quickblox.com"
qbChatNick = qbUserID

jid = qbChatLogin
password = qbUserPass
nick = qbChatNick

counter = 0

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class MUCBot(sleekxmpp.ClientXMPP):

    """
    A simple SleekXMPP bot that will greet those
    who enter the room, and acknowledge any messages
    that mention the bot's nickname.
    """

    def __init__(self, jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.room = room
        self.nick = nick

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The groupchat_message event is triggered whenever a message
        # stanza is received from any chat room. If you also also
        # register a handler for the 'message' event, MUC messages
        # will be processed by both handlers.
        self.add_event_handler("groupchat_message", self.muc_message)
        
        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)

        # The groupchat_presence event is triggered whenever a
        # presence stanza is received from any chat room, including
        # any presences you send yourself. To limit event handling
        # to a single room, use the events muc::room@server::presence,
        # muc::room@server::got_online, or muc::room@server::got_offline.
        self.add_event_handler("muc::%s::got_online" % self.room,
                               self.muc_online)


    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        # If a room password is needed, use:
                                        # password=the_room_password,
                                        wait=True)

    def message(self, msg):
        """
        [ 1:1 CHATS. In this section we handle private (1:1) chat messages received by our bot. These may include system messages such as MUC invitations. ]
        """
        
        """
        1:1 message test auto-reply
        Uncomment the code lines below to make chat bot reply to any incoming 1:1 chat messages by quoting them
        """
        
        """
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()
        """
        
        """
        MUC auto-join:
        Let's listen for any MUC invites and join the corresponding MUC rooms once invited.
        """
        
        """if msg['mucnick'] != self.nick and "created a group" in msg['body']:"""
        if msg['mucnick'] != self.nick and "Create new chat" in msg['body']:
            from bs4 import BeautifulSoup
            y = BeautifulSoup(str(msg))
            roomToJoin = y.xmpp_room_jid.string
            print ("Got an invite to join room")
            """os.system(selfPath + " -d -j " + qbChatLogin + " -r " + str(roomToJoin) + " -n " + qbChatNick + " -p " + qbUserPass)"""
            subprocess.call(selfPath + " -d -j " + qbChatLogin + " -r " + str(roomToJoin) + " -n " + qbChatNick + " -p " + qbUserPass, shell=True)

            self.send_message(mto=msg['from'].bare,
                          mbody="Thank you for your kind invitation, joining your new room now!",
                          mtype='groupchat')



    def muc_message(self, msg):
        """
        [ MUC CHATS. In this section we handle messages from MUC (multi-user chat rooms) our bot participates in. ]
        """
        
        """
        Process incoming message stanzas from any chat room. Be aware
        that if you also have any handlers for the 'message' event,
        message stanzas may be processed by both handlers, so check
        the 'type' attribute when using a 'message' event handler.
        """

        """
        Whenever the bot's nickname is mentioned, respond to
        the message.

        IMPORTANT: Always check that a message is not from yourself,
                   otherwise you will create an infinite loop responding
                   to your own messages.

        This handler will reply to messages that mention
        the bot's nickname.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """

        if msg['mucnick'] != self.nick and self.nick in msg['body']:
            self.send_message(mto=msg['from'].bare,
                      mbody="I heard that, %s." % msg['mucnick'],
                      mtype='groupchat')


        """
        Reply to anyone's test message (any message containing "test" in it)
        """

        if msg['mucnick'] != self.nick and "test" in msg['body']:
            self.send_message(mto=msg['from'].bare,
                      mbody="Test passed, %s." % msg['mucnick'],
                      mtype='groupchat')


        """
        Repeat every 3rd message in the room. Useful for testing.
        """
        global counter
        if msg['mucnick'] != self.nick:
            counter += 1
        
        if counter == 3:
            self.send_message(mto=msg['from'].bare,
                              mbody="Let me repeat that: %s." % msg['body'],
                              mtype='groupchat')
            counter = 0



    def muc_online(self, presence):
        """
        Process a presence stanza from a chat room. In this case,
        presences from users that have just come online are
        handled by sending a welcome message that includes
        the user's nickname and role in the room.

        Arguments:
            presence -- The received presence stanza. See the
                        documentation for the Presence stanza
                        to see how else it may be used.
        """
        if presence['muc']['nick'] != self.nick:
            self.send_message(mto=presence['from'].bare,
                              mbody="Hello, %s %s" % (presence['muc']['role'],
                                                      presence['muc']['nick']),
                              mtype='groupchat')


if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
    optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

    # JID and password options.
    optp.add_option("-j", "--jid", dest="jid",
                    help="JID to use")
    optp.add_option("-p", "--password", dest="password",
                    help="password to use")
    optp.add_option("-r", "--room", dest="room",
                    help="MUC room to join")
    optp.add_option("-n", "--nick", dest="nick",
                    help="MUC nickname")

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

 if jid is None and opts.jid is None:
        jid = raw_input("Username: ")
    if password is None and opts.password is None:
        password = getpass.getpass("Password: ")
    if opts.room is None:
        opts.room = raw_input("MUC room: ")
    if nick is None and opts.nick is None:
        nick = raw_input("MUC nickname: ")

    # Setup the MUCBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = MUCBot(jid, password, opts.room, nick)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")
