#!/usr/bin/env python
# coding: utf-8

# In[1]:


from urllib.parse import urlparse
from urllib.request import urlopen
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import re
import sys
import time


# In[12]:


url='https://jobs.citizensbank.com/job/loudonville/associate-licensed-relationship-banker/288/10789840'


# In[13]:


driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get(url)
time.sleep(5)
html = driver.page_source
soup=BeautifulSoup(html)


# In[14]:


text = soup.findAll("div",{"class","ats-description"})


# In[8]:


text


# In[17]:


final_text = re.sub("\<(.*?)\>"," ",str(text))


# In[18]:


final_text


