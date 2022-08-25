#!/usr/bin/env python
""" Data Collector

Collects data from the product contained in the URL
The data is then stored inside JSON files in /products and /reviews directories."""

import json
import os
import random
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from init_dict import (
    init_product_dict, init_reviews_dict
)

# Set driver options to avoid detection
OPTIONS = Options()

# User agent
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 ' \
             'Safari/537.36 '
OPTIONS.add_argument(f'user-agent={user_agent}')
OPTIONS.add_argument("--headless")

# Disable unnecessary functionality causing message error in the console
OPTIONS.add_argument("--disable-extensions --disable-gpu --disable-dev-shm-usage --disable")
OPTIONS.add_experimental_option('excludeSwitches', ['enable-logging'])

# Closing some unnecessary pop-ups
OPTIONS.add_argument("--no-first-run --no-service-autorun --password-store=basic")

# Start in full-screen with a defined window size
OPTIONS.add_argument("window-size=1920,1080")
OPTIONS.add_argument("start-maximised")

# Hide some bot related stuff to increase stealthiness
OPTIONS.add_argument('--disable-blink-features=AutomationControlled')
OPTIONS.add_experimental_option('useAutomationExtension', False)
OPTIONS.add_experimental_option("excludeSwitches", ['enable-automation'])

# Set paths
# PATH_DRIVER = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
PATH_PRODUCT = os.path.join(os.curdir, 'products')
PATH_REVIEWS_TEST = os.path.join(os.curdir, 'reviews')
PATH_URLS_NEW = os.path.join(os.curdir, 'urls_new')
PATH_DRIVER = os.path.join(os.curdir, 'chromedriver')

# setting the driver
driver = webdriver.Chrome(PATH_DRIVER, options=OPTIONS)


# ---------------------------------------------------
# ----                  PRODUCT                  ----
# ---------------------------------------------------

def collect_product_data():
    """"
    Collects data of the product from the page and saves the data into .json files in the product directory
    """

    # Initialising the product dictionary and the list of dictionaries
    product_dict = init_product_dict()
    product_data = []

    # Loading the page and handling the cookies for the page
    try:
        driver.get('https://us.feelunique.com/p/Paulas-Choice-Resist-Perfectly-Balanced-Foaming-Cleanser-190ml')
        print("[LOG] Loading the page.")
        cookie_btn = WebDriverWait(driver, 10).until(ec.presence_of_element_located((
            By.ID, 'notice-ok')))
        cookie_btn.click()
        print("[LOG] Click on the cookies button.")
        time.sleep(random.uniform(1, 5))
    except:
        pass

    print("[LOG] Collecting product data.")

    # Product name
    try:
        product_dict['product_name'] = driver.find_element(
            By.CSS_SELECTOR, 'h1[class="fn"]').text
    except:
        pass

    # Product information
    try:
        product_dict['product_information'] = driver.find_element(
            By.CSS_SELECTOR, 'div[class="Layout-golden-main"]').text
    except:
        pass

    # Product price
    try:
        product_dict['product_price'] = driver.find_element(
            By.CSS_SELECTOR, 'span[class="Price"]').text
    except:
        pass

    # Review count
    try:
        product_dict['n_reviews'] = driver.find_element(
            By.CSS_SELECTOR, 'span[class="Rating-count"]').text
    except:
        pass
    # Product brand
    try:
        product_dict['brand'] = str(driver.find_element(
            By.CSS_SELECTOR, 'p[class="u-flush-v"]').text.split(' ')[1:])

    except:
        pass
    # Product url
    try:
        product_dict['product_url'] = driver.current_url
        print(product_dict['product_url'])
    except:

        pass
    # mean rating
    try:
        product_dict['mean_rating'] = driver.find_element(
            By.CSS_SELECTOR, 'span[class="Rating-average"]').get_attribute('data-aggregate-rating')
        print(product_dict['mean_rating'])
    except:
        print("no")
        pass

    product_data.append(product_dict)
    print("[LOG] Saving the product data.")

    # Saving product data
    with open(os.path.join(PATH_PRODUCT, str(time.strftime('%Y_%m_%d_%H_%M_%S')) + '_product.json'),
              'w', encoding='utf-8') as file_to_dump:
        json.dump(product_data, file_to_dump, indent=4, ensure_ascii=False)


# ---------------------------------------------------
# ----                  REVIEWS                  ----
# ---------------------------------------------------
def collect_reviews_data():
    # List of dictionary of reviews
    reviews_data = []

    while True:
        # Retrieving the reviews
        try:
            reviews = WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located((
                By.CSS_SELECTOR, 'ol[class*="bv-content-list-reviews"] > li')))

        except KeyboardInterrupt:
            exit("[LOG] The collect has been interrupted by the user.")

        except TimeoutException:
            print("[LOG] There aren't any reviews on the current page.")
            pass

        except Exception as e:
            print(e)
            pass

        for i, review in enumerate(reviews):
            # Initialising the reviews dict
            review_dict = init_reviews_dict()

            # Review rating
            try:
                review_dict['review_rating'] = review.find_element(
                    By.CSS_SELECTOR, 'meta[itemprop="ratingValue"]').get_attribute('content')
            except:
                pass

            # Review title
            try:
                review_dict['review_title'] = review.find_element(
                    By.CSS_SELECTOR, 'h3[class="bv-content-title"]').text
            except:
                pass

            # Review author
            try:
                review_dict['review_author'] = review.find_element(
                    By.CSS_SELECTOR, 'span[class="bv-author"]').text
            except:
                pass

            # Review content
            try:
                review_dict['review_text'] = review.find_element(
                    By.CSS_SELECTOR, 'div[class="bv-content-summary-body-text"]').text
            except:
                pass

            # Review date
            try:
                review_dict['review_date'] = review.find_element(
                    By.CSS_SELECTOR, 'span[class="bv-content-datetime-stamp"]').text.strip()
            except:
                pass

            reviews_data.append(review_dict)
        print("[LOG] Saving all the reviews data.")

        # Saving the reviews data
        with open(os.path.join(PATH_REVIEWS_TEST, str(time.strftime('%Y_%m_%d_%H_%M_%S')) + '_reviews_test.json'),
                  'w', encoding='utf-8') as file_to_dump:
            json.dump(reviews_data, file_to_dump, indent=4, ensure_ascii=False)

        print("[LOG] All the reviews on this page were collected.")

        # Clicking on the next slide button
        try:
            more_reviews_btn = WebDriverWait(driver, 10).until(ec.presence_of_element_located((
                By.CSS_SELECTOR, 'li[class*="buttons-item-next"] > a[class*="bv-content-btn-pages-active"]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", more_reviews_btn)
            driver.execute_script("arguments[0].click();", more_reviews_btn)
            print("[LOG] Click on show more reviews button.")
            time.sleep(random.uniform(1, 5))

        except TimeoutException:
            print("[LOG] There isn't any more reviews to show.")
            break

        except KeyboardInterrupt:
            print("[LOG] The collect has been interrupted by the user.")
            break

        except:
            break


def main():
    collect_product_data()
    #collect_reviews_data()

    driver.quit()


if __name__ == "__main__":
    main()
