#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
import requests
import lxml
from bs4 import BeautifulSoup


# In[8]:


URL = "https://yoshops.com/products?page=1"


# In[9]:


HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'Accept-Language':'en-US, en;q=0.5'})


# In[10]:


webpage = requests.get(URL, headers=HEADERS)


# In[11]:


type(webpage.content)


# In[49]:


soup = BeautifulSoup(webpage.content, 'html.parser')


# In[56]:


names=[]
for i in soup.find_all('span', attrs={'class':'product-title'}):
    string = i.text
    names.append(string.strip())


# In[65]:


reviews=[]
for i in soup.find_all('span', attrs={'class': 'sr-only'}):
    string=i.text
    reviews.append(string.strip())


# In[66]:


for i in reviews:
    print(i)


# In[ ]:




