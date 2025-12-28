# import
import requests
import webbrowser
import os

# clear on run
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
clear()

banner = r"""
███╗░░██╗░█████╗░░██████╗░█████╗░  ██████╗░██╗░█████╗░████████╗██╗░░░██╗██████╗░███████╗  ░█████╗░███████╗
████╗░██║██╔══██╗██╔════╝██╔══██╗  ██╔══██╗██║██╔══██╗╚══██╔══╝██║░░░██║██╔══██╗██╔════╝  ██╔══██╗██╔════╝
██╔██╗██║███████║╚█████╗░███████║  ██████╔╝██║██║░░╚═╝░░░██║░░░██║░░░██║██████╔╝█████╗░░  ██║░░██║█████╗░░
██║╚████║██╔══██║░╚═══██╗██╔══██║  ██╔═══╝░██║██║░░██╗░░░██║░░░██║░░░██║██╔══██╗██╔══╝░░  ██║░░██║██╔══╝░░
██║░╚███║██║░░██║██████╔╝██║░░██║  ██║░░░░░██║╚█████╔╝░░░██║░░░╚██████╔╝██║░░██║███████╗  ╚█████╔╝██║░░░░░
╚═╝░░╚══╝╚═╝░░╚═╝╚═════╝░╚═╝░░╚═╝  ╚═╝░░░░░╚═╝░╚════╝░░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝╚══════╝  ░╚════╝░╚═╝░░░░░

████████╗██╗░░██╗███████╗  ██████╗░░█████╗░██╗░░░██╗
╚══██╔══╝██║░░██║██╔════╝  ██╔══██╗██╔══██╗╚██╗░██╔╝
░░░██║░░░███████║█████╗░░  ██║░░██║███████║░╚████╔╝░
░░░██║░░░██╔══██║██╔══╝░░  ██║░░██║██╔══██║░░╚██╔╝░░
░░░██║░░░██║░░██║███████╗  ██████╔╝██║░░██║░░░██║░░░
░░░╚═╝░░░╚═╝░░╚═╝╚══════╝  ╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░
"""

def container():
    prints() # prints all headings
    date, url, explain, title = parser() # set variables
    # print contents
    print(title)
    print(date)
    print(explain)
    ask(url)

def parser():
    # variables
    api_key = "HsvOI2hZx8vz19tNk9TY8eVJEB2dFOM5OjWud0Lj"
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
    
    # fetch
    response = requests.get(url)
    # parse the JSON content into a dictionary
    content = response.json()
    # extract the specific fields
    date = content.get('date')
    apod_url = content.get('url')
    explanation = content.get('explanation')
    title = content.get('title')
    return date, apod_url, explanation, title

def prints():
    print(banner)
    print("(s u p e r  g e n e r i c)\n")

def ask(link):
    ans = input('Open image in your browser? [y/n]').strip().lower()
    if ans == "": ans = 'y'
    if ans in ('y', 'yes'):
        webbrowser.open(link)
    elif ans in ('n', 'no'):
        print('Exiting, be back soon.')
    else:
        print('Weird option chosen. Be back soon.')

# run
container()