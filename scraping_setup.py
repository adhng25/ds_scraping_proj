#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 02:40:28 2023

@author: honganh
"""

import linkedin_scraper as ls
import pandas as pd

# link = 'https://www.linkedin.com/jobs/entry-level-analyst-jobs?keywords=Entry%20Level%20Analyst&location=United%20States&locationId=&geoId=103644278&f_TPR=r2592000&position=1&pageNum=0'
# swe
# link = 'https://www.linkedin.com/jobs/new-grad-software-jobs?keywords=New%20Grad%20Software&location=United%20States&locationId=&geoId=103644278&f_TPR=r604800&position=1&pageNum=0'
# data
link = 'https://www.linkedin.com/jobs/search?keywords=Graduate%20Data%20Science&location=United%20States&locationId=&geoId=103644278&f_TPR=r604800&f_SB2=2&position=1&pageNum=0'

df = ls.get_jobs(10, link)
df.to_csv('linkedin-jobs.csv')