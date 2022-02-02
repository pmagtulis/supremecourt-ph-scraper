# supremecourt-ph-scraper

# What is this?

A Python scraper of the Philippine Supreme Court [e-library](https://elibrary.judiciary.gov.ph/) which is a repository of court decisions since 1996.
This is an auto-scraper that automatically collects new information from the website every Sunday and updates information in the CSV. 

# Recent updates

This is currently being developed. One initial problem noticed is the length of time it takes for the scraper to get information per each case link.
Suggestions are welcome.

A sample data frame (that which generates a summary of all cases, dates, links and GR nos.) was provided.

# What is this for?

The ideal final output of this project should be able to answer the following questions and more:

* How many cases are decided by the court each month/year, on average?
* Which justice has written the most decisions?
* How has each justice voted in each case?
* Which division of the court has disposed of most cases?

More practically, the output here should allow the use to search random cases and know how the case was decided and other pertinent matters in an instant.

# Definition of terms

The following information were scraped from the website:

|column name|definition|
|---|---|
|**case_no.**|a unique identifier to each case most commonly begins with the letters **GR**.| 
|**title**|title of the case including the plaintiff's and the defendants' names|
|**date**|date of promulgation of the court decision|
|**division**|division of the Supreme Court which handled the case. Each division typically consists of 3 to 4 members, including a chairperson. Full court deliberations are referred to as **en banc**|  
|**ponente**|the name of the justice in charge of writing the decision for the majority|

# Contact

Prinz Magtulis, [ppm2130@columbia.edu](mailto:ppm2130@columbia.edu)

**Comments and suggestions are always welcome! All rights reserved.**
