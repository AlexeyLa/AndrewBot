# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 18:09:59 2017

@author: a.lantsov
"""

import requests
from bs4 import BeautifulSoup
import time

def get_Baks():

    cur_date = time.strftime("%d.%m.%Y")
    
    url_baks = "http://mfd.ru/currency/"
    
    page = requests.get(url_baks)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    my_items = soup.find_all('td')
    my_items = [e for e in my_items if e.string!=None]
    
    
    for i,item in enumerate(my_items):
        if (item.string):
            if (len(item.string)>1)&(cur_date in item.string):
                result = (my_items[i+1].string)
    
    answer = "Бакс сегодня " + result
    return answer
