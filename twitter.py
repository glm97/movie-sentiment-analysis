from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

#consumer key, consumer secret, access token, access secret.
ckey="lQF2T05PqyUFJ3Hf20NQNGpMq"
csecret="a5oXiTf4hl6sQfvsyus0DlJUhD8eLRc6yp5fjFWM5bNXgQCTKC"
atoken="834546034210648064-b3ybwBj2uiIomTXDVZDgXt0Mt0R9Wqn"
asecret="3TwpyEu9kClHlfoeX17PnIAP747HcfxZ2GXbj3okWinwV"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        print(tweet)
        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Avengers"])