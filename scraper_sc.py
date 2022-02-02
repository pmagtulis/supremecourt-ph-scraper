#!/usr/bin/env python
# coding: utf-8

# # Philippine Supreme Court decisions
# 
# Source: https://elibrary.judiciary.gov.ph/
# 
# Background: The Supreme Court of the Philippines is the final arbiter of all constitutional petitions. It is composed of 15 magistrates appointed by the president from a list of candidates by the Judicial and Bar Council, an intersectoral and constitutional body.
# 
# In terms of deliberating on cases, the high court may raffle cases to specific divisions composed of three to four justices as members, or it can decide to discuss a case **en banc**, meaning **full court** where the 15 justices decide. Case are decide by a simple majority.
# 
# The Supreme Court maintains a database of cases found on the link above. The cases are listed based on date of promulgation of the decision of the case. **Important caveat:** the data only dates back to 1996. The court was established in 1901 and underwent some changes since then because of the changes in the Constitution, martial law era, etc.
# 
# The latest Constitution over which the court gets its authority to govern was ratified in 1986.
# 
# ### What can you do with this?
# 
# The ideal final output of this project should be able to answer the following questions, among others:
# 
# * How many cases are decided by the court each month/year, on average?
# * How many cases involve the Marcoses?
# * How has each justice voted in each case?
# 
# More practically, the output here should allow the easy search of random cases via case numbers or title, as well as easy locating of actual decisions.
# 
# This notebook, once finalized, will be turned into an auto-scraper. It will be supplemented by a separate notebook on the analysis of Supreme Court cases.

# ## Do your imports
# 
# This will be atypically longer than usual since I am importing some libraries like **warnings** to remove them from the output.

# In[1]:


import pandas as pd
from requests import get
import requests
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import time
import re
import numpy as np

import warnings
warnings.filterwarnings("ignore")


# ## Use requests

# In[ ]:


raw_html = requests.get("https://elibrary.judiciary.gov.ph/", verify=False).content


# In[ ]:


soup_doc = BeautifulSoup(raw_html, "html.parser")
#print(soup_doc.prettify())


# ## Actual scraping: the 'parent link'
# 
# **Warning:** this is gonna be tedious
# 
# Now, we proceed with actual scraping. The way the Supreme Court libarary is arranged, there are links to month under each year. Each links contain **another** set of links to cases decided and promulgated that month. 
# 
# Hence, to be able to get through the case files themselves, which is what we want, we need to go through these set of links. We start with the **month links** which I termed **parent links**.

# In[ ]:


dataset1=[]
container = soup_doc.find("div", {"id": "container_date"})
every_row = container.find_all('a')
for row in every_row:
    data={}
    data ['parent_link'] = row.attrs['href']
    dataset1.append(data)
dataset1


# Strictly speaking, you don't need to generate a data frame out of this since each case have an assigned link as well, which we can just grab for our dataframe. But if you want to, you can also grab these ones (although that is unnecessary work).

# ## Case summaries
# 
# So after grabbing all links containing a list of cases decided each month, we now turn to the **specific** case links. These case links contain some vital information we would like to scrape so that we don't need to do the same once we're **inside** each link.

# In[ ]:


dataset2=[]
for case in dataset1[0:]:
    href = case['parent_link']
    raw_html = requests.get(href, verify=False).content
    doc = BeautifulSoup(raw_html, "html.parser")
    title = doc.find("div", {"id": "container_title"})
    segments = title.find('ul')
    subheads = segments.find_all('li')
    for subhead in subheads:
        info={}
        info['case_no'] = subhead.find('strong').text
        info['title'] = subhead.find('small').text.strip()
        info['date'] = subhead.find('small').next_sibling
        info['case_link'] = subhead.find('a').attrs['href']
        dataset2.append(info)
#dataset2


# ## Transform lists of dicts to dataframe

# In[ ]:


df = pd.DataFrame(dataset2)
df


# ## Save to CSV
# 
# Saving your data frames into CSV for future reference.

# In[ ]:


df.to_csv("sc-cases.csv", index=False)

