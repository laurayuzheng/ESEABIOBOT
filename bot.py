# -*- coding: utf-8 -*-
# Copyright (c) 2015–2016 Molly White
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from bs4 import BeautifulSoup
import urllib.request
import os
import tweepy
from secrets import *
from time import gmtime, strftime
import random
import time
import re

# ====== Individual bot configuration ==========================
bot_username = ''
logfile_name = bot_username + ".log"

# ==============================================================

#random delay 30-60
#delay between loops 120 seconds 
#posts about 3 times an hour
delay = False

def create_tweet():
    """Create the text of the tweet you want to send."""
    # Replace this with your code!
    #text = ""
    # return text

    rand_delay = 0

    while True:
        #rand_delay = random.randint(90,120)
        rand_delay = 2
        id = random.randint(10000,2011007)
        #id = 1210333
        url = 'https://play.esea.net/users/%d' % id

        class AppURLopener(urllib.request.FancyURLopener):
            version = "Mozilla/5.0"
        opener = AppURLopener()
        req = opener.open(url)
        content = req.read()
        soup = BeautifulSoup(content, "html.parser")

        biography = soup.find(text="Biography")
        try:
            bio_tag = biography.parent
        except AttributeError:
            if delay:
                time.sleep(rand_delay)
            continue
        bio_content = bio_tag.findNext('div')

        size = len(bio_content.contents) - 1
        something = bio_content.contents[0]

        if size > 0:
            text = something + str(bio_content.contents[1]).strip()
        else:
            text = something

        text2 = text.replace('<br>','').replace('<br/>','').replace('</br>','') #.replace('<a href="','').replace('" rel="nofollow noopener noreferrer" target=\'_blank"\'>','').replace('</a>',' ')
        text3 = re.sub('"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"', '', text2).replace('<a href= rel="nofollow noopener noreferrer" target=\'_blank"\'>','').replace('</a>',' ')
        temp = text3[:279] #.replace('<br>','').replace('<br/>','').replace('</br>','')
        #print(temp)

        if temp.isspace() == False and temp != "":
            print(id)
            return temp
            break

        if delay:
            time.sleep(rand_delay)

    #return text
    #for d in div_class:
    #    if d.text == 'Biography':
    #        text = d.nextSibling.text
    #        return text


def tweet(text):
    """Send out the text as a tweet."""
    # Twitter authentication
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Send the tweet and log success or failure
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted: " + text)


def log(message):
    """Log message to logfile."""
    path = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)


if __name__ == "__main__":
    #while 1:
    tweet_text = create_tweet()
    print(tweet_text)
    tweet(tweet_text)
    if delay: 
        time.sleep(60*60*6)
