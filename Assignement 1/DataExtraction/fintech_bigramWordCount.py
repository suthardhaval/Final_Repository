#!/usr/bin/env python
# coding: utf-8

# In[2]:


import nltk
import re


# In[3]:


from nltk.corpus import stopwords


# In[4]:


from collections import Counter


# In[5]:


from nltk.collocations import *
import xlwt
import csv


# In[6]:


stop_words = set(stopwords.words('english'))


# In[ ]:





# In[35]:


f = open("noisy_text_data.txt","r",encoding="utf8")


# In[8]:


with open('noisy_text_data.txt', 'r',encoding="utf8") as myfile:
    data=myfile.read().replace('\n', ' ')


# In[9]:


data1 = data.replace('\xa0',' ')


# In[10]:


data1 = data1.replace("\''","'");


# In[11]:


data1= data1.replace(","," ")


# In[12]:


data1 = data1.replace(";"," ")


# In[13]:


data1 = data1.replace("."," ")


# In[14]:


data1 = data1.replace("|"," ")


# In[ ]:





# In[15]:


data1 = data1.lower()


# In[16]:


data1 = re.sub("[^a-zA-Z']"," ",data1)


# In[17]:


data1 = data1.replace("www"," ")


# In[18]:


data1 = data1.replace("https"," ")


# In[ ]:





# In[19]:


nltk_tokens = nltk.word_tokenize(data1)


# In[40]:


nltk_tokens


# In[20]:

import custom_stopwords

filtered_sentence = [w for w in nltk_tokens if not w in custom_stopwords.stop_words_list] 


# In[21]:


filtered_sentence


# In[41]:


bigram_list_with_sw= list(nltk.bigrams(nltk_tokens))


# In[43]:


bigram_list_with_sw


# In[44]:


order_pair_with_sw = Counter(bigram_list_with_sw).most_common()


# In[47]:


tup_list_with_sw=[]
for lists in order_pair_with_sw:
    word1 = lists[0][0]
    word2 = lists[0][1]
    count = lists[1]
    final = (word1+' '+word2)
    tup = (final,count)
    tup_list_with_sw.append(tup)  

# In[ ]:





# In[ ]:





# In[ ]:





# In[23]:


bigram_list = list(nltk.bigrams(filtered_sentence))


# In[117]:


for pair in bigram_list:
    pairs = pair
    print(pairs)


# In[131]:


order_pair = Counter(bigram_list).most_common()


# In[ ]:





# In[168]:


tup_list=[]
for lists in order_pair:
    word1 = lists[0][0]
    word2 = lists[0][1]
    count = lists[1]
    final = (word1+' '+word2)
    tup = (final,count)
    tup_list.append(tup)  


# In[140]:


with open('bigram_wordCount.csv', 'w',encoding="UTF-8") as csvFile:
    writer = csv.writer(csvFile, lineterminator='\n')
    writer.writerows(order_pair)
csvFile.close()


# In[169]:


tup_list


# In[170]:


with open('bigram_wordCount.csv', 'w',encoding="UTF-8") as csvFile:
    writer = csv.writer(csvFile, lineterminator='\n')
    writer.writerows(tup_list)
csvFile.close()