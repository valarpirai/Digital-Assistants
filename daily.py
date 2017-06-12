import wx
import os
# os.environ["HTTPS_PROXY"] = "http://user:pass@192.168.1.107:3128"
import wikipedia
import wolframalpha
import time
import webbrowser

import json
import requests
import ctypes
import random
from bs4 import BeautifulSoup

from urllib.request import urlopen
import speech_recognition as sr
import ssl
# Remove SSL error
requests.packages.urllib3.disable_warnings()

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)\
           AppleWebKit/537.36 (KHTML, like Gecko)\
           Chrome/53.0.2785.143 Safari/537.36'}

# GUI creation
class MyFrame(wx.Frame):
    def __init__(self):
        
        print('''Welcome back Sir, Broono at your service.''')
        while True:
            self.OnEnter()

    def OnEnter(self):
        print("Listening for command")
        put = '' # self.txt.GetValue()
        put = put.lower()
        link = put.split()
        if put == '':
            r = sr.Recognizer()
            with sr.Microphone() as src:
                audio = r.listen(src)
            try:
                put = r.recognize_google(audio)
                put = put.lower()
                link = put.split()
                # self.txt.SetValue(put)
                print("Command : ")
                print(put)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google STT; {0}"
                      .format(e))
            except Exception as e:
                print(e)
                print("Unknown exception occurred!")

# Open a webpage
        if put.startswith('open '):
            try:
                print("opening "+link[1])
                webbrowser.open('http://www.'+link[1]+'.com')
            except Exception as e:
                print(e)
                print('Sorry, No Internet Connection!')
# Play Song on Youtube
        elif put.startswith('play '):
            try:
                link = '+'.join(link[1:])
                say = link.replace('+', ' ')
                url = 'https://www.youtube.com/results?search_query='+link
                source_code = requests.get(url, headers=headers, timeout=15)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, "html.parser")
                songs = soup.findAll('div', {'class': 'yt-lockup-video'})
                song = songs[0].contents[0].contents[0].contents[0]
                hit = song['href']
                print("playing "+say)
                webbrowser.open('https://www.youtube.com'+hit)
            except Exception as e:
                print(e)
                print('Sorry, No internet connection!')
# Google Search
        elif put.startswith('search '):
            try:
                link = '+'.join(link[1:])
                say = link.replace('+', ' ')
                # print(link)
                print("searching on google for "+say)
                webbrowser.open('https://www.google.co.in/search?q='+link)
            except Exception as e:
                print(e)
                print('Sorry, No internet connection!')

# News
        elif put.startswith('science '):
            try:
                jsonObj = urlopen('''https://newsapi.org/v1/articles?source=new-scientist&sortBy=top&apiKey=your_API_here''')
                data = json.load(jsonObj)
                i = 1
                print('''Here are some top science
                             news from new scientist''')
                print('''             ================NEW SCIENTIST=============
                      '''+'\n')
                for item in data['articles']:
                    print(str(i)+'. '+item['title']+'\n')
                    print(item['description']+'\n')
                    i += 1
            except Exception as e:
                print(e)
                print('Sorry, No internet connection')
        elif put.startswith('headlines '):
            try:
                jsonObj = urlopen('''https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=your_API_here''')
                data = json.load(jsonObj)
                i = 1
                print('here are some top news from the times of india')
                print('''             ===============TIMES OF INDIA============'''
                +'\n')
                for item in data['articles']:
                    print(str(i)+'. '+item['title']+'\n')
                    print(item['description']+'\n')
                    i += 1
            except Exception as e:
                print(e)
                print(str(e))

# # Other Cases
#         else:
#             pass
#             try:
#                 # wolframalpha
#                 client = wolframalpha.Client(app_id)
#                 res = client.query(put)
#                 ans = next(res.results).text
#                 print(ans)
#                 print(ans)
#             except Exception as e:
#                 print(e)
#                 # wikipedia
#                 put = put.split()
#                 put = ' '.join(put[2:])
#                 #print(put)
#                 print(wikipedia.summary(put))
#                 print('Searched wikipedia for '+put)


# Trigger GUI
if __name__ == "__main__":
    frame = MyFrame()

