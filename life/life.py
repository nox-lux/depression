# IMPORTS
import os
import random
import time
from colorama import init, Fore
from datetime import date
from pathlib import Path
from rich.console import Console

# CLEAR ON RUN
clear = lambda: os.system("cls" if os.name == "nt" else "clear")
clear()


# INIT RICH AND COLORAMA
console = Console()
init(autoreset=True)

# BANNER THAT TAKES UP LOT OF SPACE
banner = r"""
██╗░░░░░██╗███████╗███████╗
██║░░░░░██║██╔════╝██╔════╝
██║░░░░░██║█████╗░░█████╗░░
██║░░░░░██║██╔══╝░░██╔══╝░░
███████╗██║██║░░░░░███████╗
╚══════╝╚═╝╚═╝░░░░░╚══════╝
"""

# TAKE DATE
def takeDate():
    D = int(input("Date: "))
    M = int(input("Month: "))
    if D > 12:
        print("There aren't more than 12 months...")
        return
    if M in (4,6,9,11) and date > 30:
        print("This month has only 30 days...")
        return
    Y = int(input('Year: '))
    if Y > date.today().year: 
        print("Were you born in the future!?")
        return
    return D, M, Y

# HOW OLD?
def daysOld():
    d,m,y = takeDate()
    birth_date = date(y,m,d)
    today = date.today()
    return (today - birth_date).days

# PATH-SETTER
def quotesPath():
    BASE_DIRECTORY = Path(__file__).resolve().parent
    quotes = BASE_DIRECTORY / "quotes.txt"
    return quotes
def stuffPath():
    BASE_DIRECTORY = Path(__file__).resolve().parent
    quotes = BASE_DIRECTORY / "stuff_you_should_hear.txt"
    return quotes

# RUN EVERYTHING
def container():
    # PRINT
    print(Fore.LIGHTYELLOW_EX+banner, end="")
    with open(quotesPath(), "r", encoding="utf-8") as f: print(random.choice(f.readlines()), end="")
    # ASK
    print("*************************************************\n"+"When were you born?")
    # FETCH DAYS
    days = daysOld()
    with console.status("You have lived for...", spinner="aesthetic"): time.sleep(1.5)
    console.print(days, "days!")
    time.sleep(2)
    # STUFF YOU SHOULD HEAR
    with console.status("Let's talk about something else...", spinner="hearts"): time.sleep(3)
    with open(stuffPath(), "r", encoding="utf-8") as f:
        clear()
        for i in f.readlines():
            print(Fore.LIGHTCYAN_EX+i, end="")
            time.sleep(4)
    print("")
    with console.status("Let me clean up!", spinner="boxBounce"):
        time.sleep(3)
        clear()

container() # RUN