# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 15:06:01 2021

@author: Diego Garcia
"""

from selenium import webdriver
import time
import pandas as pd

class Rooftop:
    database = pd.read_csv('data_rooftop.csv',index_col=0)
    links = []
    street = []
    city = []
    state = []
    zipcode = []
    rooms = []
    areas = []
    ages = []
    prices = []
    rents = []
    rate = []
    gyield = []
    ratings = ['"rating_1"','"rating_2"','"rating_3"','"rating_4"','"rating_5"']
    rating = []
    df = pd.DataFrame() #First create a csv file containing the columns of the dataframe
    
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.filterpage()
        self.getNpages()
        
        if self.page != 0:
            self.getLinks()
            for i in range (0,(self.page-1)):
                self.browser.execute_script("window,scrollTo(0,120);")
                time.sleep(1)
                if i <= 1:
                    next_section= self.browser.find_element_by_xpath('(//li[contains(@class,"emxLdE")])[6]')
                    next_section.click()
                elif i > 1 and i < self.page-2:
                    next_section= self.browser.find_element_by_xpath('(//li[contains(@class,"emxLdE")])[7]')
                    next_section.click()
                else:
                    next_section= self.browser.find_element_by_xpath('(//li[contains(@class,"emxLdE")])[6]')
                    next_section.click()
                time.sleep(1.5)
                self.getLinks()
     
        
        self.getFirstUpdates()
        self.getData()
        self.dataframe()
        self.save_data()
        
    def filterpage(self):
        self.browser.get('https://www.roofstock.com/investment-property-marketplace')
        time.sleep(2)
        
        filter_applied = self.browser.find_element_by_xpath('//*[contains(text(),"More")]')
        filter_applied.click()
        time.sleep(1)
        For_Sale = self.browser.find_element_by_xpath('(//*[contains(text(),"For Sale")])[3]')
        For_Sale.click()
        time.sleep(2)
        Check_All = self.browser.find_element_by_xpath('//input[@value="All"]')
        Check_All.click()
        time.sleep(1)
        Apply_click = self.browser.find_element_by_xpath('//*[contains(text(),"Apply")]')
        Apply_click.click()
        time.sleep(1)
                
    def getLinks(self):
        links = self.browser.find_elements_by_xpath("//a[@target='_self']")
        condition = lambda link: '.com/investment-property-details/' in link.get_attribute('href')
        valid_links = list(filter(condition,links))
            
        for i in range(len(valid_links)):
            link = valid_links[i].get_attribute('href')
            if link not in self.links:
                self.links.append(link)
                
    def getNpages(self):
        n_page = self.browser.find_element_by_xpath('(//li[contains(@class,"emxLdE")])[5]').text
        self.page = int(n_page)
        
    def getFirstUpdates(self):
        links_previous = self.database['Links']
        actual_links = pd.DataFrame(self.links,columns=['Actual Links'])
        update = ~actual_links['Actual Links'].isin(links_previous)
        confirm = any(update)
        #new_links = actual_links(update)
        if confirm == True:
            print('There are new items to add to the data frame, Do you want to update it? Y/N \n')
            while True:
                x=input()
                if x == 'Y' or x =='y' or x=='Yes':
                    new_links = actual_links[update]
                    #print(new_links)
                    self.links = new_links['Actual Links'].tolist()
                    break
                elif x=='N' or x=='n' or x=='No':
                    print('the data was not updated and a new frame is going to be created')
                    self.links = self.links
                    break
                else:
                    print("Please input Yes/No.")
    
            
                
    def getData(self):
        for index,link in enumerate(self.links):
            self.browser.get(link)
            time.sleep(0.5)
            
            self.getAddress()
            #time.sleep(1)
            
            self.getRooms()
            #time.sleep(1)
            
            self.getPrice()
            #time.sleep(1)
            
            self.getCurrentrent()
            #time.sleep(1)
            
            self.getCapRate()
            #time.sleep(1)
            
            self.getGrossYield()
            #time.sleep(1)
            
            self.getRating()
            #time.sleep(1)
            
            #if index == 3:
                #break
    
    def getAddress(self):
        address = self.browser.find_element_by_xpath('//div[contains(@class,"ListingHeaderstyle__AddressContainer-sc-1h7il48-6 ")]')
        street = address.find_element_by_tag_name('p')
        street_name = street.get_attribute('innerHTML')
        self.street.append(street_name)
        
        city = address.find_element_by_tag_name('h6').text
        
        #get city
        j=0
        city_name = ''
        for i in range(len(city)):
            if city[i] != ',':
                city_name = city_name + city[i]
                j = i+3
            elif city[i] == ',':
                break         
        self.city.append(city_name)
        
        #get states
        states = ''
        for i in city[j:]:
            if i != ' ':
                states = states + i
                k=j+3
            elif i == ' ':
                break
        self.state.append(states)
        
        #get zipcodes
        zipcodes = ''
        for i in city[k:]:
            zipcodes = zipcodes + i
        self.zipcode.append(zipcodes)
    
    def getRooms(self):
        r = self.browser.find_element_by_xpath('//div[@class="CarouselContainer"]').text
        j=0
        room = ''
        for i in range(len(r)):
            if r[i] !='|':
                room = room + r[i]
                j=i+2
            elif r[i]=='|':
                break
        self.rooms.append(room)
        
        #get sqft
        area = ''
        for i in r[j:]:
            if i != 's':
                area = area + i
                #k=j+23
            elif i == 's':
                break
        self.areas.append(area)
        
        #get home age
        '''age = ''
        try: 
            for i in r[k:]:
                age = age + i
            self.ages.append(age)
        except:
            self.ages.append(age)'''
        age = self.browser.find_element_by_xpath('//div[@class="CarouselContainer"]').text[-4:]
        self.ages.append(age)
        
    
    def getPrice(self):
        Pr = self.browser.find_element_by_xpath('//span[contains(@class,"jVQRaZ")]')
        price = Pr.get_attribute('innerHTML')
        self.prices.append(price)
    
    def getCurrentrent(self):
        rent = self.browser.find_element_by_xpath('(//div[@style="float: right;"])[3]').text
        self.rents.append(rent)
    
    def getCapRate(self):
        rates = self.browser.find_element_by_xpath('(//div[@style="float: right;"])[6]').text
        self.rate.append(rates)

    def getGrossYield(self):
        gyields = self.browser.find_element_by_xpath('(//div[@style="float: right;"])[7]').text
        self.gyield.append(gyields)                
    
    def getRating(self):
        totalstar=0
        for rating in self.ratings:
            search = self.browser.find_element_by_xpath('//label[@for='+rating+']')
            time.sleep(1)
            star = search.get_attribute('class')
            if "dv-star-rating-full-star" not in star:
                filter1 = search.find_element_by_xpath('//span')
                filter2 = filter1.get_attribute('innerHTML')
                if "position: absolute;" not in filter2:
                    totalstar = totalstar + 0
                else:
                    totalstar = totalstar + 0.5
            else:
                totalstar = totalstar + 1
        self.rating.append(totalstar)
            
    
    def dataframe(self): 
        self.df = pd.DataFrame(list(zip(self.street,self.city,self.state,self.zipcode,self.rooms, self.areas, self.ages,
                                   self.prices,self.rents,self.rate,self.gyield,self.rating,self.links)), 
               columns =['Street', 'City','State','Zip','Rooms','sqft area','Built in','Price','Current Rents',
                         'Cap Rate','Gross Yield','Rating','Links'])
        self.df =pd.concat([self.df,self.database],ignore_index=True)
        self.df['Street'] = self.df.Street.str.replace('<br>', '')
        #print(self.df)
        
    def save_data(self):
        self.df.to_csv('data_rooftop.csv',index=False)

rooftop = Rooftop()