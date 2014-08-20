<h2>TestBot: a QuickBlox compatible chat bot</h2>

This is a basic chat bot code that works in both 1:1 and MUC chat environments.
Can be used for adding automated agents into QuickBlox powered apps. 
Typical use cases include testing, moderation, customer support, trivia/quiz games etc.

<h3>How to start</h3>
start the bot by running the shell command:
<pre>python [FULL PATH]/testbot.py -r [room JID]</pre>
example: python /Work/chatbot/testbot.py -d -r 7232_53baafe7535c1282fe019dda@muc.chat.quickblox.com

alternatively you may specify full parameters in command line
<pre>python [FULL PATH]/testbot.py -j [user JID] -r [room JID] -n [QB user ID] -p [QB user PASSWORD]</pre>

if you omit the parameters, the script will ask you to enter manually.

<h3>MUC auto-join</h3>
for MUC auto-join to work, you need to update the QB credentials in testbot.py and also make it executable (shell: chmod -x testbot.py).

<h3>Logging options</h3>
Add these to command line for various logging options:
'-q', '--quiet': set logging to ERROR
'-d', '--debug': set logging to DEBUG
'-v', '--verbose': set logging to COMM


