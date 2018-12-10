from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import json

import tkinter as tk
from tkinter import *

#Plots
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time

#Nosso modulos
import naiveBayes as nb
import liveplot

#Chaves de acesso
ckey="lQF2T05PqyUFJ3Hf20NQNGpMq"
csecret="a5oXiTf4hl6sQfvsyus0DlJUhD8eLRc6yp5fjFWM5bNXgQCTKC"
atoken="834546034210648064-b3ybwBj2uiIomTXDVZDgXt0Mt0R9Wqn"
asecret="3TwpyEu9kClHlfoeX17PnIAP747HcfxZ2GXbj3okWinwV"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        sentiment_value, confidence = nb.sentiment(tweet)
        print(tweet,'\n', sentiment_value,'\n', confidence)
        if confidence*100 >= 80:
            #tweetsOut = open("twitter-out.txt","a", encoding='utf-8')
            #tweetsOut.write(tweet)
            #tweetsOut.write('\n')
            #tweetsOut.close()

            confidenceOut = open("twitter-confidence.txt","a", encoding='utf-8')
            confidenceOut.write(sentiment_value)
            confidenceOut.write('\n')
            confidenceOut.close()
        return(True)

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)


#twitterStream.filter(track=["Avengers"])

f = Figure(figsize=(5,4), dpi=100)

style.use("ggplot")
ax1 = f.add_subplot(1,1,1)
print("Fig and Ax1 DONE")

def animate(i):
    pullData = open("twitter-confidence.txt","r").read()
    lines = pullData.split('\n')

    xar = []
    yar = []

    x = 0
    y = 0

    for l in lines[-50:]:
        x += 1
        if "pos" in l:
            y += 1
        elif "neg" in l:
            y -= 1
        xar.append(x)
        yar.append(y)
        
    ax1.clear()
    ax1.plot(xar,yar)


def button_click():
    # função que usa o texto de entrada para filtrar tweets
    print("Fetching tweets...")
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=[str(ed.get())])
    print("Setting canvas...")
    canvas = FigureCanvasTkAgg(f, master=janela)
    canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    canvas = FigureCanvasTkAgg(f, master=janela)
    ani = animation.FuncAnimation(f, animate, interval=1000)
    



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