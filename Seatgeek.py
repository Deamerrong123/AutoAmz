import os
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from collections import defaultdict

URL = 'https://seatgeek.com/mayday-tickets/brooklyn-new-york-barclays-center-2022-11-19-8-pm/concert/r/5729854'
DRIVER_PATH = os.path.join('utility', 'edgedriver_linux64', 'msedgedriver')
EMAIL = "deamerrong123@gmail.com"
PASSWORD = "520QZrong!"
SEARCHING = "MAYDAY"
SCROLL_PAUSE_TIME = 0.5
STARTING_POINT = 6


def Grap_data():
    tickets = []
    driver = webdriver.Edge(DRIVER_PATH)
    wait = WebDriverWait(driver, 10)
    driver.implicitly_wait(15)
    driver.get(URL)

    something = wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="start-of-content"]/div[1]/div/header/div[2]/p')))
    # will need to perform scrolling with this ActCObj
    a = ActionChains(driver)
    a.move_to_element(something).click().send_keys(Keys.PAGE_DOWN).perform()

    k = STARTING_POINT
    while True:
        try:
            ticket = {}
            # get the info for Seat
            XPATH = f'//*[@id="start-of-content"]/div[1]/div/div[{k}]/div/div/div/div[2]/div[3]/p'
            Seat = wait.until( EC.presence_of_all_elements_located((By.XPATH, XPATH)))[0]
            ticket.update({'Seat': Seat.text})  # update to ticket

            # get the info for price.
            XPATH = f'//*[@id="start-of-content"]/div[1]/div/div[{k}]/div/div/div/div[2]/div[1]/h3/span'
            price = wait.until(EC.presence_of_all_elements_located((By.XPATH, XPATH)))[0].text
            ticket.update({'Price': price})
            tickets.append(ticket)  # update ticket into tickets

            # increment for selector
            k = k + 1
            a.move_to_element(Seat).send_keys(Keys.PAGE_DOWN).perform()
        except TimeoutException as exception:
            print("Can't not locate elements")
            break
    return tickets



if __name__ == '__main__':


        '''
        //*[@id="start-of-content"]/div[1]/div/header/div[2]/p
        '''

        '''
        //*[@id="start-of-content"]/div[1]/div/div[6]/div/div/div/div[2]/div[1]/h3/span
        '''
        '''
        //*[@id="start-of-content"]/div[1]/div/div[5]/div/div/div/div[2]/div[3]/p
        //*[@id="start-of-content"]/div[1]/div/div[6]/div/div/div/div[2]/div[3]/p
        '''
        # SAVE DATA.
        with open("result.json",'w') as f:
                json.dump(tickets, f)
        # END.
        print("Load completed")

        driver.quit()

