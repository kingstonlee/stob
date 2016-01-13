class Speech():
    def __init__(self, sourcemessage, sourcechannel):
        targettext = "beep boop"
        print sc.api_call("chat.postMessage", as_user="true", channel=sourcechannel, text=targettext)
