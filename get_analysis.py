# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 10:25:53 2021

@author: Diego Garcia
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd


df = pd.read_csv('data_rooftop.csv')


def getAnalysis(df):
    highlights={'Roof':[],'Attic':[],'Bathrooms':[],'Basement':[],'HVAC':[],'Bedrooms':[],'Electrical':[],
              'Exterior':[],'Garage':[],'Plumbing':[],'Landscaping':[],'Structural':[],'Kitchen':[]}
    browser = webdriver.Chrome()
    x=1
    for index,link in enumerate(list(df['Links'])):
        browser.get(link)
        time.sleep(0.85)
        
        try:
            analysis = browser.find_element_by_xpath('(//button[contains(@class,"MuiTab-root")])[3]')
        except NoSuchElementException:
            x=0
            for highlight in highlights.values():
                highlight.append('--')
            pass
        
        if x!=0: 
            analysis.click()
            for i,highlight in enumerate(highlights.values()):
                x= browser.find_element_by_xpath('(//div[contains(@class,"MuiGrid-grid-xs-6")])['+str(i+1)+']//span').text
                highlight.append(x)
        x=1
        '''if index == 10:
            break'''
    
    df2=pd.DataFrame.from_dict(highlights)
    df2.to_csv('highlights_rooftop.csv',index=False)
    
    return df2
        
        
        