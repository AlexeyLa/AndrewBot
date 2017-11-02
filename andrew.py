# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 17:20:47 2017

@author: a.lantsov
"""

import json 
import requests
import time
#import page_dollar_scraping
from dbhelper import DBHelper
#import requests
#from bs4 import BeautifulSoup
#import time

db = DBHelper()


TOKEN = "415764410:AAHePZcdnTdp81URghm2czq2v_vxsd6C-X8"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
text2  = "чо с баксом?"
chat = 219156205

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset = None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)
    
def handle_updates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            items = db.get_items()
            if text in items:
                db.delete_item(text)
                items = db.get_items()
            else:
                db.add_item(text)
                items = db.get_items()
            message = "\n".join(items)
            send_message(message, chat)
        except KeyError:
            pass

def main():
    while True:
        text, chat = get_last_chat_id_and_text(get_updates())
        if (text.lower() == "чо с баксом?"):
            baks = 150
#            baks = page_dollar_scraping.get_Baks()
            send_message("ща...", chat)
            time.sleep(5)            
            send_message(baks, chat)
#        if (text, chat) != last_textchat:
#            send_message(text, chat)
#            last_textchat = (text, chat)
        time.sleep(5)

if __name__ == '__main__':
    main()