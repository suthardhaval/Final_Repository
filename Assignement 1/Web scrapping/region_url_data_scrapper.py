#!/usr/bin/env python
# coding: utf-8

# In[126]:


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


# In[173]:


url='https://regions.wd5.myworkdayjobs.com/en-US/Regions_Careers/job/PlazaDallas/Mortgage-Loan-Originator--Greater-Dallas-Area_R23531-1'


# In[174]:


driver = webdriver.Chrome(executable_path='C:/Users/kiran/Documents/chromedriver.exe')
driver.get(url)
time.sleep(5)
html = driver.page_source
soup=BeautifulSoup(html)


# In[175]:


body = soup.findAll("div",{"class","GWTCKEditor-Disabled"})[1]


# In[176]:


body


# In[177]:


body = BeautifulSoup(str(body))


# 

# In[132]:


for text in body.findAll("span"):
    text1 = BeautifulSoup(str(text))
    text2 = text1.find('span').get_text()
    print(text2)


# In[178]:


body1 = str(body).replace("<span><span>","")


# In[179]:


body2 = str(body1).replace("</span></span>","")


# In[138]:


for text in BeautifulSoup(body2).findAll("span"):
    text1 = BeautifulSoup(str(text))
    text2 = text1.find('span').get_text()
    print(text2)


# In[180]:


body2


# In[204]:


span10 = []
for span3 in BeautifulSoup(body2).findAll("p"):
    span4 = BeautifulSoup(str(span3))
    span5 = span4.find("p").get_text()
    span10.append(span5)
    print(span5)


# In[166]:


BeautifulSoup(body2).findAll("p",attrs={"dir":"LTR"})


# In[206]:


for span in BeautifulSoup(body2).findAll("li"):
    span1 = BeautifulSoup(str(span))
    span2 = span1.find("li").get_text()
    span10.append(span2)
    print(span2)


# In[201]:


span6 = str(span2)+str(span5)


# In[209]:


for d in span10:
    print(d)


# In[ ]:
