# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 17:40:12 2016

@author: dmitrys
"""

###############################################################
####       Meme parsing just for lulz and science  <3      ####
###############################################################


import re
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
from urllib.request import Request, urlopen
import getpass
import sys
sys.path.append('/Users/dmitrys/anaconda2/lib/python2.7/site-packages')
username = getpass.getuser()

#### Send me a letter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from email.mime.base import MIMEBase
#from email import encoders
import requests
import sys


#### GOING TO TOR
import socks
import socket
socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
socket.socket = socks.socksocket
#print(urlopen('http://icanhazip.com').read())


from fake_useragent import UserAgent

def generateUserAgent():
    return UserAgent().chrome

def html_stripper(text):
    return re.sub('<[^<]+?>', '', str(text))


number_of_pages = 369
page = 1
main_url = 'http://knowyourmeme.com/'
columns = ['name', 'added', 'views', 'comments', 'status', 'year', 'tags', 'about', 'origin', 'spread']
FINAL = pd.DataFrame(columns=columns)
START = time.time()

def getMemeUrls(page):
    req = Request('http://knowyourmeme.com/memes/all/page/{}'.format(page), headers={'User-Agent': generateUserAgent()})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "lxml")
    meme_urls = soup.findAll('a', attrs={'class':'photo'})
    print('Getting all memes from page {}'.format(page))
    return meme_urls



def getAllFromPage(meme_urls):
    global FINAL
    count = 0
    start = time.time()
    current_shape = FINAL.shape
    for meme in meme_urls:
        count += 1

        
        to_append = {x:np.NaN for x in columns}
        #time.sleep(1)
        try:
            meme_url = re.split('href="|" target="|"> <img|"', str(meme))[3]
            meme_page = Request(main_url+meme_url, headers={'User-Agent': generateUserAgent()})
            meme_page = urlopen(meme_page).read()
            meme_page = BeautifulSoup(meme_page, 'lxml')
        except:
            continue
        #### NAME & DATE
        try:
            raw = html_stripper(meme_page.find('section', attrs={'class':'info'})).split('\n')
            for i in raw:
                if i!='':
                    name = i
                    break
            for j in range(len(raw)-1):
                if raw[j] == 'Added':
                    added = raw[j+1]
            
            to_append['name'] = name
            to_append['added'] = added
        except:
            name = 'NULL'
            continue
        
        #### VIEWS
        try:
            views = meme_page.find('dd', attrs = {'class':'views'})
            views = re.split('title="| Views"', str(views))[1].replace(',', '')
            to_append['views'] = views
        except:
            continue
        
        #### COMMENTS
        try:
            comments = meme_page.find('dd', attrs = {'class':'comments'})
            comments = re.split('title="| Comments"', str(comments))[1]
            to_append['comments'] = comments
        except:
            continue
        
        #### PROPERTIES
        try:
            properties = meme_page.find('aside', attrs = {'class':'left'})
            properties = html_stripper(properties).split('\n')
            properties = [x for x in properties if x != '']
            
            status = properties[1]
            year = properties[3]
            tags = properties[7]
            
            to_append['status'] = status
            to_append['year'] = year
            to_append['tags'] = tags
        except:
            continue
        #### ABOUT & ORIGINS & SPREAD
        try:
            raw = html_stripper(meme_page.find('section', attrs = {'class':'bodycopy'})).split('\n')
            about, origin, spread = ('', '', '')
            for i in range(len(raw)-1):
                if raw[i] == 'About':
                    about = raw[i+1]
                elif raw[i] == 'Origin':
                    origin = raw[i+1]
                elif raw[i] == 'Spread':
                    spread = raw[i+1]
                    
            to_append['about'] = about
            to_append['origin'] = origin
            to_append['spread'] = spread
        except:
            continue
        #print('got {} meme!'.format(name))


        sys.stdout.write("Meme number:   {}\r".format(count))
        sys.stdout.flush()
        
        

        FINAL = FINAL.append(to_append, ignore_index=True)
        
    #### Now if we've been banned, send a letter and wait!
    if FINAL.shape == current_shape:
        print("Dayum son, something's wrong!")
        raise ValueError
        #unban = input('Gonna send`em? (y/n)')
        unban = 'n'
        if unban=="y":
                   
            IP = requests.request('GET', 'http://myip.dnsomatic.com').text
            
            fromaddr = "MYMAIL"
            msg = MIMEMultipart()
             
            msg['From'] = fromaddr
            #bans@knowyourmeme.com
            recipients = ['bans@knowyourmeme.com']
            print('Now sending emails to {}'.format(", ".join(recipients)))
            msg['To'] = ", ".join(recipients)
            msg['Subject'] = "{} banned".format(IP)
             
        
            # Fooling around with the message <3
            import random
            foo = ['Hi, please unban {}!', 
                   'Sorry, working on a parsing project, please unban {}!', 
                   'Sorry again, could you unban {}?', 
                   'Hi, working on a parse project, please unban {}', 
                   'Please, unban {}', 
                   'Hi, could you, please, unban {} again?']
            body = random.choice(foo).format(IP)
            msg.attach(MIMEText(body, 'plain'))
                     
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "PASSWORD")
            text = msg.as_string()
            server.sendmail(fromaddr, recipients, text)
            server.quit()
            print("Sent, now waiting for 30 mins")
            time.sleep(1800)

        else:
            print("End of parsing")
            raise ValueError
        
    print('Total memes got {}'.format(count))
    print('elapsed time: {} sec'.format(round(time.time()-start, 1)))
    print('========')


#for page in range(1, number_of_pages):
#    print(re.split('href="|" target="|"> <img|"', str(getMemeUrls(page)[10]))[3])
START_PAGE = int(input("enter the start page"))
for page in range(START_PAGE, number_of_pages):
    try:
        #IP = urlopen(Request('http://icanhazip.com', headers={'User-Agent': generateUserAgent()})).read()
        #print("Current IP is {}".format(IP))
        getAllFromPage(getMemeUrls(page))
        FINAL.to_csv('/Users/{}/Desktop/DataProjects/KnowYourMemes/{}'.format(username, 'Memes_final_second.csv'))
        time.sleep(15)
    except ValueError:
        try:
            print("Let's try again")
            print("Current page is {}".format(page))
            #print("Current IP is {}".format(IP))
            time.sleep(600)
            getAllFromPage(getMemeUrls(page))
        except ValueError:
            FINAL.to_csv('/Users/{}/Desktop/DataProjects/KnowYourMemes/{}'.format(username, 'Memes_{}.csv'.format(page)))
            break
        
FINAL.to_csv('/Users/{}/Desktop/DataProjects/KnowYourMemes/{}'.format(username, 'Memes.csv'))
print('Finished!')
print('Total time: {}'.format((time.time() - START)/60))