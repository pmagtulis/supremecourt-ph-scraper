# %%
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


# %% [markdown]
# ## Scraping

# %%
raw_html = requests.get("https://elibrary.judiciary.gov.ph/", verify=False).content

# %%
soup_doc = BeautifulSoup(raw_html, "html.parser")
#print(soup_doc.prettify())

# %% [markdown]
# ## Scrape the last 24 months of case files

# %%
main_link=[]
container = soup_doc.find("div", {"id": "container_date"})
every_row = container.find_all('a')
for row in every_row[:24]: 
    data={}
    data ['parent_link'] = row.attrs['href']
    main_link.append(data)
main_link

# %% [markdown]
# ## Scrape the contents of those 24 months
# 
# ### First, the case no., title, date, and link

# %%
import concurrent.futures
from tqdm import tqdm

case_container=[]
def download_decisions(decisions):
    href = decisions['parent_link']
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
        case_container.append(info)

    time.sleep(5)

def loop(download_decisions, main_link):
    no_threads = 25
    threads = min(no_threads, len(main_link))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        # you don't need this at all, 
        # this is for tqdm to work 
        # so you can track the progress 
        # of your scraper.
        list(tqdm(executor.map(download_decisions, main_link), total=len(main_link)))

loop(download_decisions, main_link)

# %% [markdown]
# ### Second, the division where the case was raffled, and the ponente

# %%
writer_division=[]
def download_url(details): 
    href = details ['case_link']
    try:
        raw_html = requests.get(href, verify=False).content
    except:
        raw_html = requests.get(href, verify=False).content
    doc = BeautifulSoup(raw_html, "html.parser")
    container = doc.find('div', {"id": "left"})
    info={}
    try:
        info['division'] = container.find('h2').text
    except:
        info['division'] = None 
    try:
        info['ponente'] = container.find('strong').text
    except:
        info['ponente'] = None 
    info['case_link'] = details['case_link']
    writer_division.append(info)

    time.sleep(5)

def run_iterator(download_url, case_container):
    no_threads = 25
    threads = min(no_threads, len(case_container))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        # you don't need this at all, 
        # this is for tqdm to work 
        # so you can track the progress 
        # of your scraper.
        list(tqdm(executor.map(download_url, case_container), total=len(case_container)))

run_iterator(download_url, case_container)

# %% [markdown]
# ## Dataframes
# 
# Put all scraped files into different dataframes and then merge with existing CSV containing older decisions.

# %%
df_summary = pd.DataFrame(case_container)
df_summary

# %%
df_details = pd.DataFrame(writer_division)
df_details

# %%
merged = df_summary.merge(df_details, suffixes=('_left'))
merged

# %% [markdown]
# ## Working with pandas
# 
# Combine the newly scraped files with existing CSV that contains decisions from 1996.

# %%
old_decisions= pd.read_csv('csv/decisions-from-1996.csv')
old_decisions

# %% [markdown]
# ## Removing duplicates
# 
# This is key here: we need to make sure that no decisions are duplicated when we merge them to ensure accuracy. The original CSV we have has data as late as **August 2021**. Therefore we only need decisions from **August 2021 upwards**.

# %%
df_combined = (pd.concat([merged, old_decisions]).drop_duplicates(subset=["case_no", "title", "date", "case_link", "division", "ponente"], keep="first").reset_index(drop=True))
df_combined

# %% [markdown]
# ## Sort according to date

# %%
df_combined.date =df_combined.date.str.replace(',', "")
df_combined.date = pd.to_datetime(df_combined.date)
df_combined

# %%
df_combined = df_combined.sort_values('date').reset_index(drop=True)
df_combined

# %%
df_combined.to_csv("csv/complete_decisions.csv", index=False)


