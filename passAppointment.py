from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import JavascriptException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import re
import time
import traceback
import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import utils

import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("info.log"),
        logging.StreamHandler()
    ]
)

def check_exists(driver, xpath):
    '''
    Returns true if element exists, false if not.
    '''
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except NoSuchElementException:
        return False
    except TimeoutException:
        return False
    return True

def setupDriver():
    '''
    Setup Chrome driver.
    '''
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--lang=de")
    options.add_argument("--window-size=1080,960")
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
    driver.set_page_load_timeout(15)
    return driver


if __name__ == '__main__':

    while True:
        for i in range(3):
            try:
                driver = setupDriver()
                driver.get("https://termine-reservieren.de/termine/leer/select2?md=2")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='collapse_btn accordion-toggle collapsed' and contains(text(), 'Ausweis- /Passangelegenheiten')]"))).click()
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[1]/div[2]/form/div/div[2]/div[2]/div[4]/div/span[2]/button"))).click()
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[1]/div[2]/form/input[4]"))).click()
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div/div[2]/div/div[1]/div/label"))).click()
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div/div[2]/div/div[2]/div/label"))).click()
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div/div[2]/div/div[3]/div/label"))).click()
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div/div[2]/div/div[4]/div/label"))).click()
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/div/div[3]/button[1]"))).click()
                time.sleep(2)
                if check_exists(driver, "//*[contains(text(), '19.07.2022')]"):
                    os.system( "say beep" )
                    os.system( "say beep" )
                    os.system( "say beep" )
                    logging.info(">>>>>>>>> Neuer Termin wäre verfügbar!")
                else:
                    logging.info(">>>>>>>>> Nichts neues.")
                break
            except ElementClickInterceptedException:
                logging.error("ElementClickInterceptedException at try: " + str(i))
            except Exception:
                logging.error("Exception at try: " + str(i))

        driver.close()
        driver.quit()
        logging.info("The program has finished.")
        time.sleep(600)
