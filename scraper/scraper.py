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
from colorama import init, Fore, Back, Style
import curses
import time
import os



# clear on run
# initialize colorama
init(autoreset=True)
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
clear()

banner= r"""
░██████╗░█████╗░██████╗░░█████╗░██████╗░███████╗██████╗░
██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
╚█████╗░██║░░╚═╝██████╔╝███████║██████╔╝█████╗░░██████╔╝
░╚═══██╗██║░░██╗██╔══██╗██╔══██║██╔═══╝░██╔══╝░░██╔══██╗
██████╔╝╚█████╔╝██║░░██║██║░░██║██║░░░░░███████╗██║░░██║
╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚══════╝╚═╝░░╚═╝
"""

# container
def container():
    print(Fore.LIGHTCYAN_EX + banner)
    print(Fore.LIGHTYELLOW_EX +"Note! Some tags might be returned empty due to it being represented with other types of data (example: images)")
    website = input("Enter a website to scrape:\n")
    try:
        driver = browser() # initialize browser
        driver.get(website)
    except Exception as e:
        if not website: print("...Where's the website?")
        else: 
            f = open("log.txt", "w")
            f.write(str(e))
            f.close()
            print("Something went wrong... Information saved in 'log.txt'")
        return

    ACTIONS = {
        "p": output_paragraphs,
        "a": output_links,
        "h": output_headings,
        "ul": output_ul,
        "ol": output_ol,
        "li": output_li,
    }

    while True:
        choice = curses_choose()
        if choice == "q":
            print("Exiting, be back soon.")
            break
        try: ACTIONS[choice](driver)
        except Exception as e:
            f = open('log.txt', 'w')
            f.writelines(str(e))
            f.close()
            print("Something went wrong... Information saved in 'log.txt'")
        input("\nEnter to continue...")

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

def output_paragraphs(driver):
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    print(f"Found {len(paragraphs)} <p> tags!")
    for p in paragraphs:
        text = p.text.strip()
        if not text: continue
        print(p.text)

def output_headings(driver):
    # go through all headings
    levels = [1,2,3,4,5,6]
    def all_headings(heading):
        headings = driver.find_elements(By.TAG_NAME, f"h{heading}")
        print(f"Found {len(headings)} <h{heading}> tags!")
        for p in headings:
            text = p.text.strip()
            if not text: continue
            print(p.text)
    for i in levels:
        all_headings(i)
    
def output_links(driver):
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"Found {len(links)} <a> tags!")
    for a in links:
        href = a.get_attribute("href")
        if href:
            print(href)

def output_ul(driver):
    ul = driver.find_elements(By.TAG_NAME, "ul")
    print(f"Found {len(ul)} <ul> tags!")
    for p in ul:
        text = p.text.strip()
        if not text: continue
        print(p.text)

def output_ol(driver):
    ol = driver.find_elements(By.TAG_NAME, "ol")
    print(f"Found {len(ol)} <ol> tags!")
    for p in ol:
        text = p.text.strip()
        if not text: continue
        print(p.text)

def output_li(driver):
    li = driver.find_elements(By.TAG_NAME, "li")
    print(f"Found {len(li)} <li> tags!")
    for p in li:
        text = p.text.strip()
        if not text: continue
        print(p.text)

def choose(stdscr):
    options = [
        ("p", "Paragraphs: <p>"),
        ("a", "Links: <a href='...'>"),
        ("h", "Headings: <h1/2/3/4/5/6>"),
        ("ul", "Unordered Lists: <ul>"),
        ("ol", "Ordered Lists: <ol>"),
        ("li", "list Item: <li>"),
        ("q", "Quit"),
    ]
    idx = 0

    curses.curs_set(0) # hide za cursor
    stdscr.keypad(True) # arrow key support

    while True:
        stdscr.clear()
        stdscr.addstr("Scrape what?\n\n", curses.A_BOLD)

        for i, (_, label) in enumerate(options):
            if i == idx:
                stdscr.addstr(f"> {label}\n", curses.A_REVERSE)
            else:
                stdscr.addstr(f"  {label}\n")

        key = stdscr.getch()

        if key == curses.KEY_UP:
            idx = (idx - 1) % len(options)
        elif key == curses.KEY_DOWN:
            idx = (idx + 1) % len(options)
        elif key in (10, 13):  # enter
            return options[idx][0]

def curses_choose(): return curses.wrapper(choose)

# run
container()