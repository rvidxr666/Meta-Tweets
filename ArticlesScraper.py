from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
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


def articles_summary(lst, browser):
    df = pd.DataFrame()
    for pack in lst:
        browser.driver.get("https://smmry.com/")
        while True:
            try:
                browser.driver.find_element_by_xpath('//input[contains(@class, "sm_force_url_alone")]').send_keys(pack[0])
                break
            except ElementNotInteractableException:
                pass
        browser.driver.find_element_by_xpath('//input[contains(@id, "sm_submit")]').click()
        sleep(5)
        while True:
            try:
                text = browser.driver.find_element_by_xpath('//div[contains(@id, "sm_secondary_inner_interface")]').text
                break
            except NoSuchElementException:
                pass

        dict_with_data = {"ArticleName":pack[1], "Summary":text, "Link":pack[0]}
        df = df.append(pd.DataFrame(dict_with_data, index=[0]))
    print(df["Summary"])


def main(art_addr):
    df = pd.DataFrame()
    browser = ScrapingBrowser(art_addr)

    while True:
        current_link = browser.driver.current_url
        browser.scroll_down()

        lst_of_links = [link.get_attribute("href") for link in browser.driver
            .find_elements_by_xpath('//div[contains(@class, "yuRUbf")]/a')]
        lst_of_articles = [link.text for link in browser.driver
            .find_elements_by_xpath('//h3[contains(@class, "LC20lb MBeuO DKV0Md")]')]
        lst_of_lsts = [list(x) for x in zip(lst_of_links, lst_of_articles)]
        articles_summary(lst_of_lsts, browser)
        browser.driver.get(current_link)
        # print(len(lst_of_lsts), lst_of_lsts)

        try:
            link = browser.driver.find_element_by_xpath('//a[contains(@id, "pnnext")]').get_attribute("href")
            browser.driver.get(link)
        except NoSuchElementException:
            break

    # browser.driver.close()


if __name__ == "__main__":
    main(
        "https://www.google.com/search?q=facebook+meta+opinion&sxsrf=AOaemvIdShQ0o70xHFfLO1BMdEFeLAar3Q%3A1642626722115&ei=on7oYf6wBvKFrwT15bDoCg&oq=facebook+meta+opinion&gs_lcp=Cgdnd3Mtd2l6EAEYADIFCAAQgAQ6BwgjEOoCECc6BAgjECc6CgguEMcBENEDEEM6BQguEJECOgsILhCABBDHARDRAzoFCC4QgAQ6BAgAEEM6CwguEIAEEMcBEK8BOgUIABCRAjoKCAAQgAQQhwIQFDoHCAAQgAQQCjoFCAAQywE6CAgAEBYQChAeOgYIABAWEB46CQgAEMkDEBYQHkoFCDwSATVKBAhBGABKBAhGGABQAFifNWDBPGgGcAB4AIABdYgB9A2SAQQyMC4ymAEAoAEBsAEKwAEB&sclient=gws-wiz")
