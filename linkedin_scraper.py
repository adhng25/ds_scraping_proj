
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 19:54:27 2023

@author: honganh
"""

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

import time
import re
import pandas as pd
import numpy as np

start_time = time.time()

def random_sleep(sleep_time):
    rs = np.random.randint(3, sleep_time)
    time.sleep(rs)

def get_jobs(sleep_time, link, email = '', password = ''):
    # set up chrome driver
    wd = webdriver.Chrome()
    
    # # your secret credentials:
    # email = 
    # password = 
    
    # # Go to linkedin and login
    # wd.get('https://www.linkedin.com/login')
    # random_sleep(sleep_time)
    # wd.find_element('id', 'username').send_keys(email)
    # wd.find_element('id', 'password').send_keys(password)
    # wd.find_element('id', 'password').send_keys(Keys.RETURN)
    
    # job link
    url = link
    wd.get(url)
    # random_sleep(sleep_time)
    time.sleep(10)
    
    # get number of jobs
    s = wd.find_element(By.CSS_SELECTOR,'h1>span').get_attribute('innerText')
    s1 = re.sub('[^0-9]','',s)
    no_of_jobs = int(s1)
    print(no_of_jobs)
    
    # browse all jobs
    i = 2
    while i <= int(no_of_jobs/25)+1: # comment out to test the code
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        i = i + 1
        try:
            scroll = wait(wd, 7).until(EC.element_to_be_clickable((By.CLASS_NAME, 
                                                                   'infinite-scroller__show-more-button')))
            scroll.click()
            random_sleep(sleep_time)
        except:
            pass
            random_sleep(sleep_time)
     
    # find the job list
    time.sleep(10)
    job_lists = wd.find_element(By.CLASS_NAME, 'jobs-search__results-list')
    jobs = job_lists.find_elements(By.TAG_NAME, 'li')
    time.sleep(5)
    
    # Extract element from job bar
    job_id= []
    job_title = []
    company_name = []
    location = []
    date = []
    job_link = []
    
    for job in jobs:
        try:
            job_id0 = job.get_attribute('data-id')
            job_id.append(job_id0)
        except NoSuchElementException:
            job_id.append(-1)
        
        try:
            job_title0 = job.find_element(By.CSS_SELECTOR,'h3').get_attribute('innerText')
            job_title.append(job_title0)
        except NoSuchElementException:
            job_title.append(-1)    
        
        try:
            company_name0 = job.find_element(By.CSS_SELECTOR,'h4').get_attribute('innerText')
            company_name.append(company_name0)
        except NoSuchElementException:
            company_name.append(-1)    
        
        try:
            location0 = job.find_element(By.CSS_SELECTOR,'[class="job-search-card__location"]').get_attribute('innerText')
            location.append(location0)
        except NoSuchElementException:
            location.append(-1) 
        
        try:
            date0 = job.find_element(By.CSS_SELECTOR,'div>div>time').get_attribute('datetime')
            date.append(date0)
        except NoSuchElementException:
            date.append(-1) 
        
        try:
            job_link0 = job.find_element(By.CSS_SELECTOR,'a').get_attribute('href')
            job_link.append(job_link0)
        except NoSuchElementException:
            job_link.append(-1) 
    
    print(len(job_id))
    print(job_id)
    print(len(job_title))
    print(len(company_name))
    print(len(location))
    print(len(date))
    print(len(job_link))
    
    # click on job title and retrieve job description
    jd = []
    seniority = []
    emp_type = []
    job_func = []
    industries = []
    
    for job in jobs:
        # clicking job to view job details
        job.click()
        
        try:
            button = wait(wd, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 
                                                                    'show-more-less-html__button')))
            button.click()
            random_sleep(sleep_time)
            
            try: 
                # find job description
                jd_class = 'show-more-less-html__markup'
                jd0 = wd.find_element(By.CLASS_NAME, jd_class).get_attribute('innerText')
                jd.append(jd0)
            except NoSuchElementException:
                jd.append(-1)
            
            try:
                # find position seniority
                seniority_path = "//ul[@class='description__job-criteria-list']/li[1]/span"
                seniority0 = wd.find_element(By.XPATH, seniority_path).get_attribute('innerText')
                seniority.append(seniority0)
            except NoSuchElementException:
                seniority.append(-1)
            
            try:
                # find employment type
                emp_type_path = "//ul[@class='description__job-criteria-list']/li[2]/span"
                emp_type0 = wd.find_element(By.XPATH, emp_type_path).get_attribute('innerText')
                emp_type.append(emp_type0)
            except NoSuchElementException:
                emp_type.append(-1)
                
            try:
                # find job functions
                job_func_path = "//ul[@class='description__job-criteria-list']/li[3]/span"
                job_func_elements = wd.find_element(By.XPATH, job_func_path).get_attribute('innerText')
                job_func.append(job_func_elements)
            except NoSuchElementException:
                job_func.append(-1)
            
            try:
                #find job industries
                industries_path = "//ul[@class='description__job-criteria-list']/li[4]/span"
                industries_elements = wd.find_element(By.XPATH, industries_path).get_attribute('innerText')
                industries.append(industries_elements)   
            except NoSuchElementException:
                industries.append(-1) 
            
            
        except:
            print('Can\'t find some elements')
            jd.append(-1)
            seniority.append(-1)
            emp_type.append(-1)
            job_func.append(-1)
            industries.append(-1) 
            pass
    
    print(len(jd))
    print(len(seniority))
    print(len(emp_type))
    print(len(job_func))
    print(len(industries))
    
    # convert data into excel file
    job_data = pd.DataFrame({'ID': job_id,
    'Date': date,
    'Company': company_name,
    'Title': job_title,
    'Location': location,
    'Description': jd,
    'Level': seniority,
    'Type': emp_type,
    'Function': job_func,
    'Industry': industries,
    'Link': job_link
    })
    # cleaning description column
    job_data['Description'] = job_data['Description'].str.replace('\n',' ')
                                                                            
    print("--- %s seconds ---" % (time.time() - start_time))
     
    return job_data
    
                                                                              
                                                                          
