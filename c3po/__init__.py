import time, random, json
from slackclient import SlackClient
from microsofttranslator import Translator

#Initial Setup information
token           = "xoxb-18158336356-XpI1LlpFhMJhTF5krPq14jJE"# found at https://api.slack.com/web#authentication
googleapikey    = "AIzaSyAlDYlziWrOP5JwNxtZxxSG56w3FKIA1C8"
msclientsecret  = "KgKKwR+UILpk0IUlZ0VaZTtBbOrXFqzsgit8y8jNK3M="
msclientid      = "c3po"
sc = SlackClient(token)

#Discover Your Surroundings
who = json.loads(sc.api_call("users.list"))['members']
#channels = json.loads(sc.api_call("channels.list"))['channels']
#dms = json.loads(sc.api_call("im.list"))['ims']
chan="C0J8WTYTF"

actives = []
for user in who:
	# Grabbing Odo's ID (to prevent loops when he talks about himself)
	if user['name'] == 'c-3po':
		c3po_id = user['id']

	if user['name'] == 'r2-d2':
		r2d2_id = user['id']
		r2d2_name = user['name']

	# Making a list of active users
	active = json.loads(sc.api_call("users.getPresence", user=user['id']))
	active = active['presence']
	if active == "active":
		actives.append(user)

#Simple Messaging
c3pouser        = 'sir'

powerons        = [ "Is there anything I might do to help?",
                "Where am I? I must have taken a bad step."]
thanks          = [ "Oh you're perfectly welcome, sir."]
shutdowns       = [ "I've got to rest before I fall apart. My joints are almost frozen.",
                    "Sir, if you'll not be needing me, I'll close down for awhile.",
                    "I don't think I can make it. You go on, Master Luke. There's no sense in you risking yourself on my account. I'm done for."]
shutup              = "Shutting up, sir."
c3pounknowns        = [ "I don't think so, sir. I'm only a droid and not very knowledgeable about such things, not on this planet, anyway. As a matter of fact, I'm not even sure which planet I'm on.",
                    "I heartily agree with you sir.",
                    "I don't like the look of this.",
                    "I don't know what all the trouble is about, but I'm sure it must be your fault." ,
                    "You watch your language!",
                    "Oh, my. I'd forgotten how much I hate space travel.",
                    ]

def C3POGreet(user, c3pochannel):
    c3pouser = '<@' + user + '>'
    greetings   = ['Hello, Master ' + c3pouser + '.',
                   'I am C-3PO, Human Cyborg Relations.']
    greeting = random.choice(greetings)
    print sc.api_call("chat.postMessage", as_user="true:", channel=c3pochannel, text=greeting)

def C3POThanks(user):
    thank       = random.choice(thanks)
    print sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=thank)

def C3POShutdown(c3pouser, c3pomessage, c3pochannel):
    shutdown    = random.choice(shutdowns)
    print sc.api_call("chat.postMessage", as_user="true:", channel=c3pochannel, text=shutdown)

def C3POShutup(user):
    print sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=shutup)

def C3POTranslate(c3pouser, c3pomessage, c3pochannel):
    translator  = Translator('c3po', 'KgKKwR+UILpk0IUlZ0VaZTtBbOrXFqzsgit8y8jNK3M=')
    message     = c3pomessage.split(' ',1)[1]
    language    = 'en'
    translated  = translator.translate(message, language)
    print sc.api_call("chat.postMessage", as_user="true:", channel=c3pochannel, text=translated)

def C3POBrain(events):
    for evt in events:
        print(evt)
        if "type" in evt:
            if evt["type"] == "message" and "text" in evt:
                c3pochannel = evt['channel']
                c3pomessage = evt["text"]
                c3pouser    = evt['user']
                if c3pomessage.startswith('translate') and evt['user'] != c3po_id:
                    C3POTranslate(c3pouser, c3pomessage, c3pochannel)
                elif "hello" in c3pomessage.lower() and evt['user'] != c3po_id:
                    C3POGreet(evt['user'],c3pochannel)
                elif "thank you" in c3pomessage.lower() and evt['user'] != c3po_id:
                    C3POThanks(evt['user'])
                elif "shut down" in c3pomessage.lower() and evt['user'] != c3po_id:
                    C3POShutdown(c3pouser, c3pomessage, c3pochannel)
                elif "shut up" in c3pomessage.lower() and evt['user'] != c3po_id:
                    C3POShutdown(evt['user'])
                elif c3po_id in c3pomessage and evt['user'] != c3po_id:
                    c3pounknown     = random.choice(c3pounknowns)
                    print sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=c3pounknown)
            if evt['type'] == 'presence_change' and evt['user'] == r2d2_id:
				if evt['presence'] == 'away':
					print 'away'
					r2away = r2d2_name + ' where are you?'
					print sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=r2away)
				elif evt['presence'] == 'active':
					print 'active'
					r2active = 'Oh, there you are ' + r2d2_name + '!'
					print sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=r2active)

if sc.rtm_connect():
    try:
        poweron     = random.choice(powerons)
        print sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=poweron)
        while True:
            events = sc.rtm_read() # print events
            C3POBrain(events)
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown    = random.choice(shutdowns)
        print sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=shutdown)
else:
    print "Connection Failed, invalid token?"
