import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

import re
from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError
from math import ceil
from random import randint
from time import sleep
from base64 import b64decode
from io import BytesIO



URL = 'https://novosibirsk.cian.ru/snyat-kvartiru-1-komn-ili-2-komn/'
count_on_page = 28

def avito_parser():
    try:
        ua = UserAgent().chrome
    except FakeUserAgentError:
        ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={ua}")
    options.add_argument("--disable-blink-features=AutomationControlled")


    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.get(URL)


    count = int(
        re.findall("\d+",
            driver.find_element(
                By.CSS_SELECTOR,'div[data-name="SummaryHeader"]'
            ).text.replace(" ","")
        )[0]
    )


    for _ in range(count // count_on_page + 1):
        offer = []
        elems = driver.find_elements(
            By.CSS_SELECTOR, 'div[data-testid="offer-card"]'
        )
        for elem in elems:
            try:
                cian_id = int(elem.get_attribute("id")[1:])
                url = elem.find_element(
                    By.CSS_SELECTOR, 'a'
                ).get_attribute("href")
                item_address = elem.find_element(
                    By.CSS_SELECTOR, value='div[data-name="SpecialGeo"]'
                ).text.split("\n")
                address = item_address[0]
                advert = elem.text.split("\n")
                price = int(advert[1][:-10].replace(" ", ""))
                rooms = advert[0].split(", ")[0].split()[0].replace("-к.", "")
                area = float(advert[0].split(", ")[1][:-3].replace(",", "."))
                floor = int(advert[0].split(", ")[2].split("/")[0])
                total_floor = int(advert[0].split(", ")[2].split("/")[1][:-4])
                text = elem.find_element(
                    by=By.CSS_SELECTOR, value='div[data-name="Description"]'
                ).get_attribute("content")

                hover = ActionChains(driver).move_to_element(elem)
                hover.perform()


                rand_sleep = randint(25, 49)
                sleep(rand_sleep / 10)


                result = (
                    cian_id,
                    rooms,
                    area,
                    price,
                    address,
                    floor,
                    total_floor,
                    text,
                    url,
                )
                offer.append(result)

            except Exception as ex:
                print(ex)

        driver.find_element(
            By.CSS_SELECTOR, 'a=["button"]'
        ).click()

    driver.quit()


if __name__ == "__main__":
    avito_parser()