from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import re

class Interact:

    def __init__(self, timeout=10) -> None:
        """

        Parameters
        ----------
        timeout : int
            max wait time (in seconds) before explicit wait times out

        Creates
        -------
        username : str
            Planbox admin username
        pw : str
            Planbox admin password matching username
        path_to_photos : str
            absolute path to location holding the user photos to upload
        driver : Selenium webdriver
            app used to navigate around the webpage
        wait : Selenium WebDriverWait
            used for explicit waits
        """
        # path to user phots
        self.path_to_photos = f"R:\\Departments\\Public\\Information Technology\\Photos\\"
        
        # driver
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        # explicit wait
        self.wait = WebDriverWait(self.driver, timeout)

    def navigate_to_webpage(self, full_site):
        """
        Navigates to the given webpage

        Parameters
        ----------
        full_site : str
            webpage url
        """
        self.driver.get(full_site)

    def enter_text(self, text, tagname, attribute, value, subtag=""):
        """
        Sends/enters text into an input

        Parameters
        ----------
        text : str
            text to send to input
        tagname : str
            html tag for xpath
        attribute : str
            html attribute for xpath
        value : str
            html value for xpath
        subtag : str, default ""
            subtag to look for in xpath - MUST include the starting "/"
        """
        self.wait.until(EC.visibility_of_element_located((By.XPATH, f"//{tagname}[@{attribute}='{value}']{subtag}"))).send_keys(text)

    def simple_click_button(self, tagname, attribute, value, subtag=""):
        """
        Clicks a button that is easily interactable with

        Parameters
        ----------
        tagname : str
            html tag for xpath
        attribute : str
            html attribute for xpath
        value : str
            html value for xpath
        subtag : str, default ""
            subtag to look for in xpath - MUST include the starting "/"
        """
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//{tagname}[@{attribute}='{value}']{subtag}"))).click()

    def click_contains(self, tagname, attribute, value):
        """
        Clicks a button that is easily interactable with

        Parameters
        ----------
        tagname : str
            html tag for xpath
        attribute : str
            html attribute for xpath
        value : str
            html value for xpath
        """
        self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//{tagname}[contains(@{attribute},'{value}')]"))).click()

    def click_on_text(self, tagname, text):
        """
        Looks for text within a given tag name to click on

        Parameters
        ----------
        tagname : str
            html tag for xpath
        text : str
            the text to look for
        """
        button = self.driver.find_element(By.XPATH, f"//{tagname}[text()='{text}']")
        self.driver.execute_script("arguments[0].click();", button)


    def java_click_button(self, tagname, attribute, value, subtag=""):
        """
        Clicks a button that typically throws a ElementNotInteractable exception

        Parameters
        ----------
        tagname : str
            html tag for xpath
        attribute : str
            html attribute for xpath
        value : str
            html value for xpath
        subtag : str, default ""
            subtag to look for in xpath - MUST include the starting "/"
        """
        button = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//{tagname}[@{attribute}='{value}']{subtag}")))\
            .find_element(By.XPATH, f"//{tagname}[@{attribute}='{value}']{subtag}")
        self.driver.execute_script("arguments[0].click();", button)

class Read:

    def __init__(self, source) -> None:
        """
        
        Parameters
        ----------
        source : web driver html source
            html source code to parse

        Creates
        -------
        soup : BeautifulSoup
            the html formatted string
        """
        self.soup = BeautifulSoup(source, 'html.parser')

    def find_class_text(self, class_str):
        """
        Finds the text from the classes in the source HTML that contain certain text

        Parameters
        ----------
        class_str : str
            sub- or full-string representing the class name

        Returns
        -------
        results : list of str
            the text from the given class
        """
        results = []
        for tab in self.soup.find_all(class_=re.compile(class_str)):
            results.append(tab.get_text())

        return results

