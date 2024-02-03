#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 18:33:09 2024

@author: honganh
"""
import pandas as pd
import numpy as np
import os
import skills_extractor as se
import job_recommendation as jr
from sklearn.neighbors import NearestNeighbors
from flask import Flask, request, jsonify
from flask_cors import CORS

def match_cv_job(file_path):
    # read job posts data
    df = pd.read_csv('processed-linkedin-jobs.csv')
    processed_jd = np.array(df['Processed_JD'])
    
    # implement knn
    tfidf = jr.skills_to_vector(file_path)
    distances, indices = jr.fit_nearest_neighbor(1, tfidf, processed_jd)
    
    # combine results to original dataframe
    matches = []
    for d in range(len(distances)):
        matches.append(distances[d][0])

    score = pd.DataFrame(matches, columns = ['Matches'])
    df['Match_score'] = score['Matches']  
    
    # return top 5 matches
    return df.head(20).sort_values('Match_score').to_json() 

def main():
    app = Flask(__name__)
    CORS(app) 
            
    @app.route('/pdf', methods=['GET'])
    def job_recommendation():
        res = match_cv_job(request.args.get('file'))
        return jsonify(res)
    
    if __name__=='__main__':
        app.run(port = 5000, debug = True)
main()