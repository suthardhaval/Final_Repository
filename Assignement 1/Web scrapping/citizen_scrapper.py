#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import sys
import time
import csv
import logging

logger = logging.getLogger(__name__)

#to get the list of urls
final_url_list = []
final_array = [[]]


driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://jobs.citizensbank.com/search-jobs')
time.sleep(10)

# driver.find_element_by_id("category-toggle").click()
# time.sleep(2)
# driver.find_element_by_id("category-filter-17").click()
# time.sleep(2)
# driver.find_element_by_id("category-filter-20").click()
# time.sleep(2)
# driver.find_element_by_id("category-filter-28").click()
# time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html,"lxml")
a_href = soup.findAll('a', href=True)
ahref_soup = BeautifulSoup(str(a_href),"lxml")
list_jobs = soup.findAll('section', id="search-results-list")
list_jobs_bs = BeautifulSoup(str(list_jobs),"lxml")
text_append = 'https://jobs.citizensbank.com'
for div in list_jobs_bs.findAll('a'):
    if div.get('class') is None:
        url = div.get('href');
        final_url = text_append+url;
        final_url_list.append(final_url)


number_of_pages = soup.findAll("span",{"class","pagination-total-pages"})[0].string

number_of_pages = re.sub("[^0-9]","",str(number_of_pages))
number_of_pages = int(number_of_pages)

for page in range(1,int(number_of_pages)):
    click_next = driver.find_element_by_xpath('//*[@id="pagination-bottom"]/div[2]/a[2]')
    click_next.click()
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html,"lxml")
    a_href = soup.findAll('a', href=True)
    ahref_soup = BeautifulSoup(str(a_href),"lxml")
    list_jobs = soup.findAll('section', id="search-results-list")
    list_jobs_bs = BeautifulSoup(str(list_jobs),"lxml")
    text_append = 'https://jobs.citizensbank.com'
    for div in list_jobs_bs.findAll('a'):
        if div.get('class') is None:
            url = div.get('href')
            final_url = text_append+url
            final_url_list.append(final_url)
driver.close()


#extract data from csv file into list : panda is a good library to read csv

import pandas as py
colname = ['rowid','words']

file_data = py.read_csv('Fintech_Wordcount_Final.csv',names = colname)

file_word = file_data.words.tolist()

#print(file_word)

#initialize an empty dictionary for storing an information 

final_dictionary = []
word_dictionary= []

i = 1 #for generating rowid for jobs

counter = 0 #for countring occurences of the words in the list

#go to each url and get the list of words 

for url in final_url_list:
    dict_count ={}
    j=0
    try:
        driver = webdriver.Chrome(executable_path='chromedriver.exe')
        driver.get(url)
        time.sleep(5)
        html = driver.page_source
        soup=BeautifulSoup(html,"lxml")
        text = soup.findAll("div",{"class","ats-description"})
        final_text = re.sub("\<(.*?)\>"," ",str(text))

        url_body = str(final_text)
        #print(url_body)
        num=100 #count for j
        for key_word in file_word[1:] :
            dict_count[key_word] = 0

        for word in file_word:
            word_nbr = final_text.count(word)
            dict_count[word] = word_nbr
        
        f_list=list(dict_count.values())
        final_array.insert(i,f_list)
        f_list.insert(0,i)
        f_list.insert(0,url)
        f_list.insert(0,i)
        f_list.insert(0,"Citizen Bank")
        f_list.insert(0,i)

        driver.close()
        i+=1

    except:
        logger.exception("Not parsable URL")
        continue    

#dump data into final CSV
csv_column = ["Job no","institution","List id","url","list id"]
for i in range(1,101):
   csv_column.append(i)

with open('Citizen_Wordcount.csv', 'w',encoding="UTF-8") as csvFile:
   writer = csv.DictWriter(csvFile, fieldnames = csv_column)
   writer.writeheader()
csvFile.close()

with open('Citizen_Wordcount.csv', 'a',encoding="UTF-8") as csvFile:
   writer = csv.writer(csvFile, lineterminator='\n')
   writer.writerows(final_array)
csvFile.close()
