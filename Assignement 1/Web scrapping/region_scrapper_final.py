#!/usr/bin/env python
# coding: utf-8

# In[11]:


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


# In[5]:


url_complete_data = ""

driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://regions.wd5.myworkdayjobs.com/Regions_Careers')
time.sleep(10)
pause=2

#click_select2 = driver.find_element_by_xpath('//*[@id="wd-FacetValue-CheckBox-c8864ef1aefc100895cbbee94d073e4b-input"]')
#click_select2.click()
#time.sleep(2)
# driver.find_element_by_class_name('WHWR').click()

# time.sleep(2)

# driver.find_element_by_id("wd-FacetValue-CheckBox-c8864ef1aefc100895cbbee94d073e4b").click()
# time.sleep(4)
# driver.find_element_by_id("wd-FacetValue-CheckBox-c8864ef1aefc100895cbca6f5fc73e4d").click()
# time.sleep(4)
# driver.find_element_by_id("wd-FacetValue-CheckBox-c8864ef1aefc100895cb66b9d89f3e2d").click()
# time.sleep(4)
# driver.find_element_by_id("wd-FacetValue-CheckBox-c8864ef1aefc100895cb996ba11f3e3d").click()
# time.sleep(4)
# driver.find_element_by_id("wd-FacetValue-CheckBox-c8864ef1aefc100895cb767714ff3e33").click()
# time.sleep(4)
# driver.find_element_by_id("wd-FacetValue-CheckBox-4b61145b4ae801449c161a4da61dc0aa").click()
# time.sleep(4)
# driver.find_element_by_id("wd-FacetValue-CheckBox-9892289d5c8d01561911e5287f0b786e").click()
# time.sleep(4)
# # In[7]:

lastHeight = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)
    newHeight = driver.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
    lastHeight = newHeight

html = driver.page_source
soup = BeautifulSoup(html,"lxml")
li_class = soup.findAll("li", { "class" : "WIYF WL3N WE5 WP-F" })
base_url = "https://regions.wd5.myworkdayjobs.com/en-US/Regions_Careers/job/"


# In[8]:


final_url_list = []
final_array = [[]]

for s in li_class:
    a = s.findAll("div",{"class","gwt-Label WPTO WJSO"})[0].string
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


# In[9]:


import pandas as py
colname = ['rowid','words']

file_data = py.read_csv('Fintech_Wordcount_Final.csv',names = colname)

file_word = file_data.words.tolist()

# print(file_word)

#initialize an empty dictionary for storing an information 

final_dictionary = []
word_dictionary= []

i = 1 #for generating rowid for jobs
#for generating rowid for word_doc
counter = 0 #for countring occurences of the words in the list
#go to each url and get the list of words 


# In[13]:
print(len(final_url_list))

for url in final_url_list:
    dict_count ={}
    url_dict_count = {}
    j=0
    try:
        
        final_string1=""
        #print(url)
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        driver.get(url)
        time.sleep(10)


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

        url_body = str(final_string1)


        url_complete_data = (url_complete_data+" "+url_body)

        # print(url_body)
        num=100 #count for j

        for key_word in file_word[1:] :
            dict_count[key_word] = 0
            
        for word in file_word:
            word_nbr = final_string1.count(word)
            dict_count[word] = word_nbr

        
        f_list=list(dict_count.values())
        f_list.insert(0,i)
        f_list.insert(0,url)
        f_list.insert(0,i)
        f_list.insert(0,"Regions Bank")
        f_list.insert(0,i)
        final_array.insert(i,f_list)


        #print(dict_count)
        
        driver.close()
        i+=1

    except:
        logger.exception("Not parsable URL")
        driver.close()
        continue    


# In[ ]:

url_complete_data = url_complete_data.encode("utf-8")

print(url_complete_data)

with open('url_complete_data.txt','w') as txtFile:
    txtFile.write(str(url_complete_data))
txtFile.close()

n=1
#print(final_array)
csv_column = ["Job no","institution","List id","url","list id"]
for n in range(100):
    csv_column.append(n)

with open('testnew.csv', 'w',encoding="UTF-8") as csvFile:
    writer = csv.DictWriter(csvFile, fieldnames = csv_column)
    writer.writeheader()
csvFile.close()

with open('testnew.csv', 'a',encoding="UTF-8") as csvFile:
    writer = csv.writer(csvFile, lineterminator='\n')
    writer.writerows(final_array)
csvFile.close()

