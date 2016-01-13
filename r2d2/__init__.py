import time, random, json
from slackclient import SlackClient
from speech import Speech

slacktoken           = "<slacktoken>"

sc = SlackClient(slacktoken)
who = json.loads(sc.api_call("users.list"))['members']

for user in who:
	# Grabbing Odo's ID (to prevent loops when he talks about himself)
	if user['name'] == 'r2-d2':
		r2d2_id = user['id']

if sc.rtm_connect():
    try:
        poweron     = "Beep beep boop"
        chan        = "C0J8WTYTF"
        print sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=poweron)
        Speech("bah", chan)
#        while True:
#            events = sc.rtm_read() # print events
#            C3POBrain(events)
#            time.sleep(1)
    except KeyboardInterrupt:
#        shutdown    = random.choice(shutdowns)
        print sc.api_call("chat.postMessage", as_user="true:", channel=chan, text=poweron)
else:
    print "Connection Failed, invalid token?"
