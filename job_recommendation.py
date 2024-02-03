#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 12:08:12 2024

@author: honganh
"""

import pandas as pd
import numpy as np
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import skills_extractor as se
vectorizer = TfidfVectorizer()

# extract dataset
df = pd.read_csv('processed-linkedin-jobs.csv')
processed_jd = np.array(df['Processed_JD'])

# extract text from pdf
def skills_to_vector(pdf_file = None):
    pdf_dir = os.getcwd()
    pdf_file = os.path.join(pdf_dir, 'CV.pdf')
    arr = se.extract_skill_from_pdf(pdf_file)
    skills = ' '.join(str(word) for word in arr)
    
    # turn skills into a vector
    tfidf = vectorizer.fit_transform([skills])
    
    return tfidf

# fit the nearest neighbors estimator on skills
def fit_nearest_neighbor(k, tfidf, job_posts):
    nbrs = NearestNeighbors(n_neighbors=k).fit(tfidf)
    job_tfidf = vectorizer.transform(job_posts)
    distances, indices = nbrs.kneighbors(job_tfidf)
    return distances, indices

# find nearest neighbors
tfidf = skills_to_vector()
distances, indices = fit_nearest_neighbor(1, tfidf, processed_jd)

# combine results to original dataframe
matches = []
for d in range(len(distances)):
    matches.append(distances[d][0])

score = pd.DataFrame(matches, columns = ['Matches'])
df['Match_score'] = score['Matches']    
    
    