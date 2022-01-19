from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import os
import re
import pandas as pd
from time import sleep
from lxml import html

path_to_the_browser = os.path.join('C:\Program Files (x86)', 'chromedriver.exe')


class ScrapingBrowser:
    path_to_the_browser = os.path.join('C:\Program Files (x86)', 'chromedriver.exe')

    def __init__(self, addr):
        self.driver = webdriver.Chrome(self.path_to_the_browser)
        self.driver.get(addr)

    def show_html(self):
        html_source = self.driver.page_source
        soup = BeautifulSoup(html_source, "html.parser")
        return soup

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)

    def get_tree(self):
        source_page = self.driver.page_source
        tree = html.fromstring(source_page)
        return tree

# def collecting_data():



def main(art_addr):
    df = pd.DataFrame()
    browser = ScrapingBrowser(art_addr)
    try:
        browser.driver.find_element_by_xpath('//button[contains(@class, "css-aovwtd")]').click()
    except NoSuchElementException:
        pass

    while True:
        browser.scroll_down()
        try:
            browser.driver.find_element_by_xpath('//div[contains(@class, "css-vsuiox")]/button').click()
        except NoSuchElementException:
            break

    browser.driver.

    browser.driver.close()


if __name__ == "__main__":
    main("https://www.nytimes.com/search?dropmab=false&endDate=20220119&query=Meta&sort=best&startDate=20211001")
