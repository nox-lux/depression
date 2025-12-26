#############################################################
'''
█░█░█ █▀█ █▀█ █▄▀   █ █▄░█   █▀█ █▀█ █▀█ █▀▀ █▀█ █▀▀ █▀ █▀ █
▀▄▀▄▀ █▄█ █▀▄ █░█   █ █░▀█   █▀▀ █▀▄ █▄█ █▄█ █▀▄ ██▄ ▄█ ▄█ ▄
'''
#############################################################

# import
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import requests

# container
def container():
    website = input('Enter a website to scrape:\n')
    driver = browser()
    content = parser(driver, website)
    output(content)
    driver.quit()

def browser():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )     
    return driver

def parser(driver, url):
    driver.get(url)
    time.sleep(3)
    return driver

def output(driver):
    required = driver.find_elements(By.TAG_NAME, "a")
    print(f"Found {len(required)} <a> tags!")
    for p in required:
        print(p.text)
# run
container()