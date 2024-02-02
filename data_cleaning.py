#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 00:42:48 2024

@author: honganh
"""

import pandas as pd
import numpy as np
from datetime import datetime
import nltk
from nltk.corpus import stopwords
stopw  = set(stopwords.words('english'))

# extract dataframe
df_data = pd.read_csv('linkedin-jobs-data.csv')
df_swe = pd.read_csv('linkedin-jobs-swe.csv')
# combine dataframe 
df = pd.concat([df_data, df_swe], ignore_index = True)
# drop unwanted columns
df = df.drop(['Unnamed: 0', 'ID'], axis = 1)
# drop duplicate rows
df = df.drop_duplicates()
# replace -1 with nan values
df = df.replace('-1', np.NaN)

# Calculate job posted duration from today
df['Date'] = pd.to_datetime(df['Date'], format = 'mixed')
duration = (datetime.today() - df['Date']).dt.days
df['Duration'] = duration.astype('int64')

# Separate state from Location column
df['Job_state'] = df['Location'].apply(lambda x: x.split(',')[1] if ',' in x else x)
df['Job_state'] = df['Job_state'].apply(lambda x: x.strip())
print(df['Job_state'].value_counts())

# Description
    # Salary Range
    # Sponsorship
    # Skills: python, SQL, Java, etc
    # no sponsor - no visa sponsor - not sponsor - require sponsor - without sponsor
    # bachelor, master, phd
    # years of experience
    # salary range
    
# Find techstack keywords from JD
df = df[df['Description'].notna()]
df['Processed_JD'] = df['Description'].apply(lambda x: ' '.join([word for word in str(x).split() if len(word)>2 \
                                                                 and word not in (stopw)]))
# df['python'] = df['Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
# df['sql'] = df['Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)
# df['R'] = df['Description'].apply(lambda x: 1 if 'r studio' or 'r-studio' in x.lower() else 0)
# df['tableau'] = df['Description'].apply(lambda x: 1 if 'tableau' in x.lower() else 0)
# df['tensorflow'] = df['Description'].apply(lambda x: 1 if 'tensorflow' in x.lower() else 0)
# df['spark'] = df['Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
# df['java'] = df['Description'].apply(lambda x: 1 if 'java' in x.lower() else 0)

# dind most frequent function, industry
most_freq_function = df['Function'].mode()[0]
most_freq_industry = df['Industry'].mode()[0]

# replace null values with most frequent one
df['Function'] = df['Function'].fillna(most_freq_function)
df['Industry'] = df['Industry'].fillna(most_freq_industry)
# replace null values with another column
df['Type'] = df['Type'].fillna(df['Level'])
print(df.info())

# Convert DataFrame to CSV file
df.to_csv(r'/Users/honganh/Dropbox/Mac/Desktop/DS_scraping_project/processed-linkedin-jobs.csv', index=False)
