import os
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep,time

## CONSTANT
URL = 'https://www.amazon.com/'
FILE = os.path.join(os.getcwd(),'LOGIN.json')
DRIVER_PATH = os.path.join('edgedriver_linux64','msedgedriver')

## public method
def login_info():
    with open(FILE,'r') as f:
        info = json.load(f)
    return info['email'] , info['passward']

## Obj class
class AutoAmaz(object):

    def __init__ (self):
        self.driver = webdriver.Edge(DRIVER_PATH)
        self.wait = WebDriverWait(self.driver,300)
        self.driver.implicitly_wait(6)
        self.driver.get(URL)

        # activate the log-in page
        self.wait.until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="nav-link-accountList"]/span'))).click()
        self.login_page()

        # navigate to "Your Account"
        self.driver.find_element(By.XPATH,'//*[@id="nav-link-accountList"]/span').click()

        # navigate to Gift cards page
        self.driver.find_element(By.PARTIAL_LINK_TEXT,"balance").click()

        # Then, redeem
        self.driver.find_element(By.LINK_TEXT,"Redeem a Gift Card").click()

    def login_page(self):
        # we need to deal with the situation
        # once we naviated to login-page
        # determine if it is login-page.
        # then, just login again.
        try:
            self.driver.find_element(By.CLASS_NAME,"a-spacing-small")

            ## prepare the login info
            email, pswd = login_info()

            ## navigate to login page...s
            ## on the login page, first is the accound name, email

            self.driver.find_element(By.ID , 'ap_email').send_keys(email,Keys.RETURN)

            ## on the passward, then enter the passward.
            self.driver.find_element(By.ID , 'ap_password').send_keys(pswd,Keys.RETURN)
            ## ...Now, we are successfully login to one account.
        except NoSuchElementException:
            print("We are not at login-page.")

            return False

        def redeem_gift_card(self,code):
            '''
            while we are on the redeem-gift-card page; locate the claim_code field, paste
            the code on the input-field. The page might be not so stable will need to login again.
            Once exceptions occurs, attaim to login.
            '''
            try:
                claim_code = self.driver.find_element(By.NAME,'claimCode')
                # paste the code on the redemption-input, and apply.
                claim_code.send_keys(code,Keys.ENTER)


                # When 'id = alertRedemptionSuccess' appear, clip 'class = a-alert-heading'
                # and driver.save_screenshot()
            except NoSuchElementException:
                self.login_page()

            finally:
                self.driver.save_screenshot(f'{code}.png')



## for testing
if __name__ == '__main__':
    acc = AutoAmaz()

