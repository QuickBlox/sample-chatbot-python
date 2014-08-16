TestBot: a QuickBlox compatible chat bot.

This is a basic chat bot code that works in both 1:1 and MUC chat environments.
Can be used for adding automated agents into QuickBlox powered apps. 
Typical use cases include testing, moderation, customer support, trivia/quiz games etc.

How to start
start the bot by running the shell command:
<pre>[FULL PATH]/testbot.py -d -j [user JID] -r [room JID] -n [QB user ID] -p [QB user PASSWORD]</pre>

Note:
for MUC auto-join to work, you need to update the QB credentials in testbot.py and also make it executable (shell: chmod -x testbot.py).

