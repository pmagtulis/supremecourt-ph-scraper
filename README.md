# supremecourt-ph-scraper

# What is this?

A Python scraper of the Philippine Supreme Court [e-library](https://elibrary.judiciary.gov.ph/) which is a repository of court decisions since 1996.
This is an auto-scraper that automatically collects new information from the website **every Sunday** and updates information in the CSV. 

# Recent updates

|date|update|
|---|---|
|*Sept 12*|Updated GitHub actions to fix Chromium problems| 
|*Feb 17*|Finally fixed the concurrent futures to scrape the division and ponente of each decision. Many thanks to the code review from Jasen!| 

# What is this for?

The ideal final output of this project should be able to answer the following questions and more:

* How many cases are decided by the court each month/year, on average?
* How many cases involved the Marcos? - this can be achieved by running regex

More practically, the output here should allow the use to search random cases and know how the case was decided by just clicking on the link of each case.

# Definition of terms

The following information are still scraped from the high court website:

|column name|definition|
|---|---|
|**case_no.**|a unique identifier to each case most commonly begins with the letters **GR**.| 
|**title**|title of the case including the plaintiff's and the defendants' names|
|**date**|date of promulgation of the court decision|
|**case_link**|link to the actual decision of the court|  
|**division**|the division of the court that rendered the decision. Typically, SC divisions are composed of three to four members| 
|**ponente**|the justice who wrote the decision who voted with the majority in the case. Only surname is provided.|  

# Requirements for use

* Python: bs4, pandas

# Contact

Prinz Magtulis, [ppm2130@columbia.edu](mailto:ppm2130@columbia.edu)

**Comments and suggestions are always welcome! All rights reserved.**
