import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from time import sleep,time

import os

URL = 'https://www.amazon.com/'
FILE = os.getcwd() + '\\login.json'

def load_login_info():
    f = open(FILE,'r')
    info = json.load(f)
    return info['email'] , info['passward']
    
    



if __name__ == '__main__':

##    PATH = os.getcwd() + '\\chromedriver.exe'
##    chrome_options = Options()
##    chrome_options.add_argument("--headless")
##    chrome_options.add_argument("--window-size=1920x1080")
##    chrome_driver = os.getcwd()+'\\chromedriver.exe'

##    browser = webdriver.Chrome('{}/chromedriver.exe'.format(os.getcwd()))
    driver = webdriver.Edge()
    driver.get(URL)
    
    ## navigate to login page...s
    driver.find_element_by_xpath('//*[@id="nav-link-accountList"]/span').click()
    ## prepare the login info
    email, pswd = load_login_info()

    ## on the login page, first is the accound name, email

    driver.find_element(By.ID , 'ap_email').send_keys(email,Keys.RETURN)

    ## on the passward page, then enter the passward.
    driver.find_element(By.ID , 'ap_password').send_keys(pswd,Keys.RETURN)
    ## ...Now, we are successfully login to one account.

    
    
    

