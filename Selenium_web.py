import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class infow():
    def __init__(self):
        self. driver= webdriver.Chrome()

    def get_info(self,query):
        self.query=query

        self.driver.get(url="https://www.wikipedia.org")
        search=self.driver.find_element("xpath","//*[@id='searchInput']")
        search.click()
        search.send_keys(query)

        for i in range(3):
            try:
                enter = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='search-form']/fieldset/button"))
                )
                enter.click()
                time.sleep(3)
                # Fetch the first paragraph of the Wikipedia article
                page_source = self.driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                paragraphs = soup.find_all('p')

                if paragraphs:
                    info = ""
                    for para in paragraphs[:5]:  # Fetch first 4-5 paragraphs
                        info += para.text
                    return info
                else:
                    return "No information found."

            except StaleElementReferenceException:
                pass





