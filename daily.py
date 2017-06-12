#!/usr/bin/env python

import os
# os.environ["HTTPS_PROXY"] = "http://username:pass@192.168.1.107:3128"
import wolframalpha
import time
import webbrowser
import json
import requests
import ctypes
import random
from bs4 import BeautifulSoup
# from urllib.request import urlopen
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
# time.sleep(2)

# GUI creation
class MyFrame():
    def __init__(self):

        wx.Frame.__init__(self, None,
                          pos=wx.DefaultPosition, size=wx.Size(450, 100),
                          style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION |
                          wx.CLOSE_BOX | wx.CLIP_CHILDREN,
                          title="BRUNO")
        panel = wx.Panel(self)

        ico = wx.Icon('boy.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
    
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        lbl = wx.StaticText(panel,
                            label="Bienvenido Sir. How can I help you?")
        my_sizer.Add(lbl, 0, wx.ALL, 5)
        self.txt = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER,
                               size=(400, 30))
        self.txt.SetFocus()
        self.txt.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
        my_sizer.Add(self.txt, 0, wx.ALL, 5)
        panel.SetSizer(my_sizer)
        self.Show()
        speak.Speak('''Welcome back Sir, Broono at your service.''')


    def OnEnter(self, event):
        put = self.txt.GetValue()

        # put = 'play oxygen from kavan' # self.txt.GetValue()
        # put = '' # self.txt.GetValue()
        # put = 'open github' # self.txt.GetValue()
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
                self.txt.SetValue(put)

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google STT; {0}"
                      .format(e))
            except:
                print("Unknown exception occurred!")

# Open a webpage
        if put.startswith('open '):
            try:
                # speak.Speak("opening "+link[1])
                webbrowser.open('http://www.'+link[1]+'.com')
            except:
                print('Sorry, No Internet Connection!')

# Play Song on Youtube
        elif put.startswith('play '):
            try:
                link = '+'.join(link[1:])
                say = link.replace('+', ' ')
                url = 'https://www.youtube.com/results?search_query='+link
                print(url)
                source_code = requests.get(url, headers=headers, timeout=15)
                plain_text = source_code.text
                soup = BeautifulSoup(plain_text, "html.parser")
                songs = soup.findAll('div', {'class': 'yt-lockup-video'})
                song = songs[0].contents[0].contents[0].contents[0]
                hit = song['href']
                # speak.Speak("playing "+say)
                webbrowser.open('https://www.youtube.com'+hit)
            except Exception,e:
                print str(e)
                print('Sorry, No internet connection!')
# Google Search
        elif put.startswith('search '):
            try:
                link = '+'.join(link[1:])
                say = link.replace('+', ' ')
                # print(link)
                speak.Speak("searching on google for "+say)
                webbrowser.open('https://www.google.co.in/search?q='+link)
            except:
                print('Sorry, No internet connection!')

# Trigger GUI
if __name__ == "__main__":
        frame = MyFrame()
