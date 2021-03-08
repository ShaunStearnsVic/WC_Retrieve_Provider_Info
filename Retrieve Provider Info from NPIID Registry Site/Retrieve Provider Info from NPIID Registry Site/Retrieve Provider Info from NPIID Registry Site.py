#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import time
import keyring
import openpyxl
from openpyxl import load_workbook
import pandas as pd
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import chromedriver_binary
from webdriver_manager.chrome import ChromeDriverManager


# ## Required Libraries
# #### os (Installed with python)
# #### time (Installed with python)
# #### keyring (conda install -c anaconda keyring)
# #### openpyxl (conda install -c anaconda openpyxl)
# #### pandas (conda install pandas)
# #### selenium (conda install -c anaconda selenium)
# #### chromedriver_binary (conda install -c conda-forge python-chromedriver-binary=87)
#    ###### NOTE: Replace "=87" with whatever version of Chrome you have running. Don't include numbers after first decimal.
# #### webdriver_manager (pip install webdriver_manager)

# # Retrieve Provider Info from NPIID Registry Site

# In[1]:


# function to take care of downloading file
def enable_download_headless(browser, download_dir):
    browser.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": download_dir},
    }
    browser.execute("send_command", params)


# instantiate a chrome options object so you can set the size and headless preference
# some of these chrome options might be uncessary but I just used a boilerplate
# change the <path_to_download_default_directory> to whatever your default download folder is located
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--verbose")
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": "<path_to_download_default_directory>",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
    },
)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")

# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
driver = webdriver.Chrome()

########################################################
# Change Path to Desired File Path
download_dir = r"C:\....\Desktop"
########################################################

# Portal Page
driver.get("https://npiregistry.cms.hhs.gov/")

# Look up provider NPIID
##########################################################################
#Change File path to Location of missing.xlsx
##########################################################################
names = pd.read_excel(r"C:\.....\missing.xlsx")
list = names["ProviderNPIID"]
#########################################################################

for i in list:
    #time.sleep(1)
    driver.find_element_by_xpath('//*[@id="508focusheader"]/div[2]/div/form/div[7]/div/div/input[1]').click()
    #time.sleep(1)
    driver.find_element_by_xpath('//*[@id="id_number"]').send_keys(i)
    #time.sleep(1)
    driver.find_element_by_xpath('//*[@id="508focusheader"]/div[2]/div/form/div[7]/div/div/input[2]').click()
    #time.sleep(1)
    name = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/table/tbody/tr/td[2]').text
    address = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/table/tbody/tr/td[4]').text
    phone = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/table/tbody/tr/td[5]').text
    print(i,",", name,",", address.split('\t'), ",", phone)
    # data to be written row-wise in csv file
    data = [[i, name, address.split('\t'), phone]] 
    # opening the csv file in 'a+' mode 
    file = open(r"C:\Users\sastearn\Desktop\missing1.csv", "a+", encoding='utf-8-sig', newline = '')
    # writing the data into the file 
    with file:     
        write = csv.writer(file) 
        write.writerows(data)
    #time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[2]/div[3]/div[2]/div/form/button').click()
    #time.sleep(1)
    driver.find_element_by_xpath('//*[@id="508focusheader"]/div[2]/div/form/div[7]/div/div/input[1]').click()

