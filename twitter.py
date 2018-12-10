from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import naiveBayes as nb
import tkinter as tk
from tkinter import *

#consumer key, consumer secret, access token, access secret.
ckey="lQF2T05PqyUFJ3Hf20NQNGpMq"
csecret="a5oXiTf4hl6sQfvsyus0DlJUhD8eLRc6yp5fjFWM5bNXgQCTKC"
atoken="834546034210648064-b3ybwBj2uiIomTXDVZDgXt0Mt0R9Wqn"
asecret="3TwpyEu9kClHlfoeX17PnIAP747HcfxZ2GXbj3okWinwV"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        sentiment_value = nb.sentiment(tweet)[0]
        confidence = nb.sentiment(tweet)[1]
        print(tweet, sentiment_value, confidence)
        if confidence*100 >= 80:
            tweetsOut = open("twitter-out.txt","a", encoding='utf-8')
            tweetsOut.write(tweet)
            tweetsOut.write('\n')
            tweetsOut.close()

            confidenceOut = open("twitter-confidence.txt","a")
            confidenceOut.write((sentiment_value,confidence))
            confidenceOut.write('\n')
            confidenceOut.close()
        print(tweet)
        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
#twitterStream.filter(track=["Avengers"])

def button_click():
    # função que usa o texto de entrada para filtrar tweets
    twitterStream.filter(track=[str(ed.get())])


janela = tk.Tk()

# label dentro de janela
lb1 = Label(janela,text= 'Movie Emotions')
lb1.place(x = 100 , y = 50)

# entrada - Onde usuario coloca o nome do filme
ed = Entry(janela)
ed.place(x=50,y=100)

bt = Button(janela,width = 10,text='Emoções!',command = button_click)
bt.place(x=200,y = 100)

# titulo
janela.title('Janela Inicial')

# cor de Fundo
# outro modo de alterar janela['bg'] = 'green'
janela['background'] = 'light blue'

# dimensoes
# Largura X altura + Distancia a esq do video + distancia do topo
# 300 x 300 + 100 + 100
janela.geometry('300x300+100+100')

janela.mainloop()


