import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
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
    

def login_page(driver):
    # we need to deal with the situation
    # once we naviated to login-page
    # determine if it is login-page.
    # then, just login again.
    try:
        driver.find_element(By.CLASS_NAME,"a-spacing-small")

        ## prepare the login info
        email, pswd = load_login_info()

        ## navigate to login page...s
        ## on the login page, first is the accound name, email

        driver.find_element(By.ID , 'ap_email').send_keys(email,Keys.RETURN)

        ## on the passward, then enter the passward.
        driver.find_element(By.ID , 'ap_password').send_keys(pswd,Keys.RETURN)
        ## ...Now, we are successfully login to one account.



    except NoSuchElementException:
        print("We are login already")

        return None

def Gift_card(driver,code):
    Entry = driver.find_element(By.ID,"gc-redemption-input")
    Entry.send_keys(code)

    # Apply to your balance
    # driver.find_element(By.ID,"gc-redemption-apply-button").click()







if __name__ == '__main__':

##    PATH = os.getcwd() + '\\chromedriver.exe'
##    chrome_options = Options()
##    chrome_options.add_argument("--headless")
##    chrome_options.add_argument("--window-size=1920x1080")
##    chrome_driver = os.getcwd()+'\\chromedriver.exe'

##    browser = webdriver.Chrome('{}/chromedriver.exe'.format(os.getcwd()))
    driver = webdriver.Edge()
    driver.implicitly_wait(1)
    driver.get(URL)

    # activate the log-in page
    driver.find_element(By.XPATH'//*[@id="nav-link-accountList"]/span').click()
    

    login_page(driver)

    # navigate to "Your Account"
    driver.find_element(By.XPATH,'//*[@id="nav-link-accountList"]/span').click()

    # navigate to Gift cards page
    driver.find_element(By.PARTIAL_LINK_TEXT,"balance").click()

    # Then, redeem
    driver.find_element(By.PARTIAL_LINK_TEXT,"redeem").click()




    
    
    
    

    
    
    

