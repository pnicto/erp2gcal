import os

from clint.textui import colored
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

os.environ["WDM_LOCAL"] = "1"


BROWSER_CHOICES = ["Chrome", "Firefox", "Edge"]


def initiate_driver_for_preferred_browser():
    print(colored.blue("Choose an installed browser among the list\n"))

    for idx, browser in enumerate(BROWSER_CHOICES):
        print(colored.magenta(f"{idx+1}. { browser }"))

    try:
        choice = int(input())
        if choice == 1:
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install())
            )
        elif choice == 2:
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install())
            )
        elif choice == 3:
            driver = webdriver.Edge(
                service=EdgeService(EdgeChromiumDriverManager().install())
            )
        else:
            raise ValueError("Invalid choice")
        return driver
    except ValueError:
        print(colored.red("Entered invalid number"))
