#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import sys
import time
import requests
import logging
import numpy as np
from array import *
import csv

logger = logging.getLogger(__name__)


# In[2]:
#if it does not work please check the path in the folder
executable_path='chromedriver.exe'
driver = webdriver.Chrome(executable_path)
driver.get('https://regions.wd5.myworkdayjobs.com/Regions_Careers')
time.sleep(10)
pause=2
'''
lastHeight = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)
    newHeight = driver.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
    lastHeight = newHeight
'''
html = driver.page_source
soup = BeautifulSoup(html,"lxml")
li_class = soup.findAll("li", { "class" : "WIYF WK3N WE5 WP-F" })
base_url = "https://regions.wd5.myworkdayjobs.com/en-US/Regions_Careers/job/"

#to get the list o urls
final_url_list = []
final_array = [[]]

for s in li_class:
    a = s.findAll("div",{"class","gwt-Label WOTO WISO"})[0].string
    c = re.sub("[^a-zA-Z0-9]","-",str(a))
    b = s.findAll("span",{"class","gwt-InlineLabel WM-F WLYF"})[0].string
    try:
        d= b.split(" | ")[0]
        d= re.sub("[^a-zA-Z0-9]","",str(d))
        e= b.split(" | ")[1]
        e= re.sub("[^a-zA-Z0-9]","",str(e))
    except:
        d='null'
        e='null'
    final_url = base_url+d+"/"+c+"_"+e
    #print(final_url)
    #append all the urls
    final_url_list.append(final_url)    
driver.close()





#extract data from csv file into list : panda is a good library to read csv

import pandas as py
colname = ['rowid','words']

file_data = py.read_csv('Fintech_TFIDF_Final.csv',names = colname)

file_word = file_data.words.tolist()

# print(file_word)

#initialize an empty dictionary for storing an information 

final_dictionary = []
word_dictionary= []

i = 1 #for generating rowid for jobs
#for generating rowid for word_doc
counter = 0 #for countring occurences of the words in the list
#go to each url and get the list of words 

for url in final_url_list[:2]:
    dict_count ={}
    url_dict_count = {}
    j=0
    try:
        
        final_string1=""
        #print(url)
        driver = webdriver.Chrome(executable_path)
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        soup=BeautifulSoup(html,"lxml")
        body = soup.findAll("div",{"class","GWTCKEditor-Disabled"})[1]
        body1 = str(body).replace("<span><span>","")
        body2 = str(body1).replace("</span></span>","")
        for text in BeautifulSoup(body2,"lxml").findAll("li"):
            text1 = BeautifulSoup(str(text),"lxml")
            text2 = text1.find('li').get_text()
            final_string1 += text2
        
        for text3 in BeautifulSoup(body2,"lxml").findAll("p"):
            text4 = BeautifulSoup(str(text3),"lxml")
            text5 = text4.find('p').get_text()
            final_string1 += text5

        url_body = final_string1.split()
        # print(url_body)
        num=100 #count for j

        for key_word in file_word[1:] :
            dict_count[key_word] = 0

        for word in url_body :
            if word in dict_count :
                dict_count[word] += 1
            else :
                pass
        

        
        f_list=list(dict_count.values())
        f_list.insert(0,i)
        f_list.insert(0,url)
        f_list.insert(0,i)
        f_list.insert(0,"Regions Bank")
        f_list.insert(0,i)
        final_array.insert(i,f_list)


        # for words in url_body:
        #     i+=1
        #     for w in file_word[1:101]:
        #         j+=1
        #         temp = { j : w}
        #         word_dictionary.append(temp.copy())
        #     j=0
        temp1 = {"job no" : i, "institution" : "Regios",
                "listid": i, "url" : url, "list" : i, "words": dict_count}   
            # final_dictionary.append(temp1.copy())   
        final_dictionary.append(temp1.copy())  
        print(dict_count)
        
        driver.close()
        i+=1

    except:
        logger.exception("Not parsable URL")
        continue    

print(final_array)
csv_column = ["Job no","institution","List id","url","list id"]
for i in range(100):
    csv_column.append(i)

with open('test.csv', 'w',encoding="UTF-8") as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames = csv_column)
    writer.writeheader()
csvFile.close()

with open('test.csv', 'a',encoding="UTF-8") as csvFile:
    writer = csv.writer(csvFile, lineterminator='\n')
    writer.writerows(final_array)
csvFile.close()