#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:28:02 2024

@author: honganh
"""
import pandas as pd
import spacy
from spacy.matcher import Matcher
import os
import PyPDF2
nlp = spacy.load("en_core_web_sm")

# extract dataframe
df = pd.read_csv('tech-skills.csv')
# remove duplication, lowercase all letters
df = df.drop_duplicates()
df = df.apply(lambda x: x.astype(str).str.lower())
skills = df.iloc[:, 0].to_numpy()

# initialize matcher
matcher = Matcher(nlp.vocab)
# create pattern
pattern = []
for s in skills:
    pattern.append([{"LOWER": s}])
# add pattern to matcher object
matcher.add("Skills", pattern)

def pdf_extractor(filepath):
    pdf_file = open(filepath, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    
    for i in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[i]
        text += page.extract_text()
    return text

def skill_extractor(text):
    doc = nlp(text)
    matches = matcher(doc)
    skills = set()
    
    for match_id, start, end in matches:
        skills.add(doc[start:end])
    return skills

def extract_skill_from_pdf(filepath):
    text = pdf_extractor(filepath)
    skills = list(skill_extractor(text.lower()))
    return skills