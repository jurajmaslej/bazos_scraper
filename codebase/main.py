import time
import re
from pprint import pprint
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

search_string = "Mercedes"
exclude_strings = set(("disky", ))
address = ""
price_from = 500
price_to = 5000
small_sleep = 0.1


def _wait(task, timeout = 10):
    value = -1
    for i in range(timeout):
        try:
            value = task()
        except:
            print('waiting')
            time.sleep(1)
    return value

def enter_value(driver, element_id, value, find_by="id"):
    if find_by == "id":
        elem = driver.find_element_by_id(element_id)
    if find_by == "name":
        elem = driver.find_element_by_name(element_id)
    elem.clear()
    time.sleep(small_sleep)
    elem.send_keys(value)


def evaluate_listing(search_string_set, listing_set, exclude_strings):
    print(listing_set)
    print(exclude_strings)
    print(f"intersection {listing_set.intersection(exclude_strings)}")
    if search_string_set.issubset(listing_set) and len(listing_set.intersection(exclude_strings)) == 0:
        return True
    return False


def check_listing_name(driver, search_string, exclude_strings=None):
    time.sleep(3)
    listing_name_href = driver.find_elements_by_xpath('//span[@class="nadpis"]/a')
    listing_price_href = driver.find_elements_by_xpath('//span[@class="cena"]/b')
    listing_price_href = [elem.text for elem in listing_price_href]
    search_string_set = set(search_string.lower().split(' '))
    good_articles = {}
    for href, price in zip(listing_name_href, listing_price_href):
        href_text = href.get_attribute('href').lower()
        price = int("".join([p for p in price if p.isdigit()]))
        a_href_set = set(re.split('/|-| |_', href_text))
        if evaluate_listing(search_string_set, a_href_set, exclude_strings):
            good_articles[href.get_attribute('href')] = price
        else:
            pass

    print(f"good adverts : ")
    pprint(good_articles)
    return good_articles


def average_pricing(good_articles):
    average = np.mean(list(good_articles.values()))
    print(f"avg price is: {average}")


def goto_next_page():
    pass


def make_search(search_string, address, price_from, price_to):
    driver = webdriver.Firefox()
    driver.get("http://www.bazos.sk")
    enter_value(driver, "hledat", search_string)
    enter_value(driver, "hlokalita", "08001")
    enter_value(driver, "cenaod", 500, find_by="name")
    enter_value(driver, "cenado", 5000, find_by="name")
    driver.find_element_by_tag_name('body').send_keys(Keys.ENTER)
    return driver


if __name__ == '__main__':
    driver = make_search(search_string=search_string, address="08001", price_from=500, price_to=5000)
    check_listing_name(driver, search_string, exclude_strings=exclude_strings)
    driver.close()