#############################################################
'''
█░█░█ █▀█ █▀█ █▄▀   █ █▄░█   █▀█ █▀█ █▀█ █▀▀ █▀█ █▀▀ █▀ █▀ █
▀▄▀▄▀ █▄█ █▀▄ █░█   █ █░▀█   █▀▀ █▀▄ █▄█ █▄█ █▀▄ ██▄ ▄█ ▄█ ▄
'''
#############################################################

# import
import requests
from bs4 import BeautifulSoup

# container
def container():
    website = input('Enter a website to scrape:\n')
    content = parser(website)
    output(content)

def parser(scrape):
    response = requests.get(scrape)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def output(soup):
    print(soup.prettify()[:1000])
    print(soup.find_all("p"))
        
# run
container()