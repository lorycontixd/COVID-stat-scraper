from modules.utility import Utility
from modules import mylogger as ml
import re
import sys,os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from xvfbwrapper import Xvfb


class App():
    def __init__(self,drivername:str):
        # Website Attributes
        self.website_main = "https://www.worldometers.info/coronavirus/"
        self.website_countries = "https://www.worldometers.info/coronavirus/#countries"
        self.cols = [
            "country",
            "total cases",
            "new cases",
            "total deaths",
            "new deaths",
            "total recovered",
            "active cases",
            "serious",
            "total Cases/1m pop",
            "deaths/1m pop",
            "total tests",
            "tests/1m pop",
            "population"
        ]

        #Class Attributes
        self.l = ml.Logger(ml.DEBUG)
        self.drivername = drivername.lower()
        self.driver = None

        #Validators
        Utility.validate_driver(drivername)
        self.connect()

    def __repr__(self):
        string = f"""
App class for Worldometers COVID scraping.
- Drivername: {self.drivername}
- Driver: {self.driver is not None}
- Logger: {self.l is not None}
"""
        return string

    def connect(self):
        if self.driver is None:
            if self.drivername != "chrome":
                exec(f"self.driver = webdriver.{self.drivername}()")
            else:
                #path = Utility.check_chromedriver(logger=self.l)
                path = '/usr/local/bin/chromedriver'
                ops = Options()
                #ops.add_argument("--headless")
                ops.add_argument("start-maximized");
                self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=ops)
                #ChromeDriverManager().install()
            self.driver.get(self.website_countries)
            self.l.info(f"Driver connected to Webdriver: {self.drivername}")
        else:
            raise ValueError("Driver is already connected")
    
    def get_table(self):
        countries = []
        elem = self.driver.find_element_by_id("main_table_countries_today")
        rows = elem.find_elements_by_xpath(".//tr/td")
        for i,row in enumerate(rows):
            if i%100==0:
                print(i," --> ",len(rows))
            text = row.text.replace(",","")
            temp = []
            if not Utility.RepresentsInt(text) and len(row.text)>0 and text!="N/A" and not Utility.RepresentFloat(text):
                #print("Not an int:\t",text)
                for k in range(13):
                    try:
                        temp.append(rows[i+k].text.replace(",",""))
                    except:
                        pass
                countries.append(temp)

        for c in countries:
            print(c)

            #print(row.text)

    def get_country(self,country:str):
        elem = self.driver.find_element_by_id("main_table_countries_today")
        rows = elem.find_elements_by_xpath(".//tr/td")
        data = []
        for i,row in enumerate(rows):
            text = row.text.replace(",","")
            if text.lower() == country.lower() and not Utility.RepresentsInt(text):
                for k in range(13):
                    try:
                        data.append( (self.cols[k],rows[i+k].text.replace(",","")) )
                    except:
                        pass
                break
        return data
    
    def get_total(self):
        elem = self.driver.find_element_by_id("main_table_countries_today")
        rows = elem.find_elements_by_xpath(".//tr/td")
        rows = rows[::-1]
        data = []
        for i,row in enumerate(rows):
            text = row.text.replace(",","")
            text = row.text.replace(":","")
            if text.lower() == "total" and not Utility.RepresentsInt(text):
                for k in range(13):
                    try:
                        data.append( (self.cols[k],rows[i-k].text.replace(",","")) )
                    except:
                        pass
                break
        return data
    
    def quit(self,code=0):
        self.driver.stop_client()
        self.driver.close()
        self.driver.quit()
        sys.exit(code)