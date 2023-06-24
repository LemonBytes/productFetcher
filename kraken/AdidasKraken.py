from random import choice
from bs4 import BeautifulSoup
from pyparsing import List
import requests
import json
from selenium import webdriver
import time


class AdidasKraken:
    def get_adidas_products(self):
    
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("window-size=1200,900")
        options.add_argument(f'--user-agent={self.get_random_useragent()}')
        browser = webdriver.Chrome(options=options)
        browser.get("https://www.adidas.de/en/performance-outlet")
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, "html.parser")
        all_a_tags = soup.find_all("a", class_="glass-product-card__assets-link")
        productList = []

        for i in range(len(all_a_tags)):
            asset = self.__get_sub_page(a_tag=all_a_tags[i], browser=browser)
            product = {
                "product_name": asset["product_name"],
                "product_link": asset["product_link"],
                "product_images": asset["product_image"],
                "product_special_price": asset["product_special_price"],
                "product_price": asset["product_price"],
            }
            productList.append(product)
        return productList
    
    
    def read_file(self, filename, method):
        with open(filename, method) as f:
            content = [line.strip('\n') for line in f]
            return content


    def get_random_useragent(self):
        useragents = self.read_file('./useragents.txt', 'r')
        return choice(useragents)

    def __get_sub_page(self, a_tag, browser):
        sales_a_tag = ""
        all_images = []
        products_name = ""
        prices = []
        SPEACIAL_PRICE = 1
        REGULAR_PRICE = 0

        browser.get("https://www.adidas.de/" + a_tag["href"])
        html_source = browser.page_source
        subpage_soup = BeautifulSoup(html_source, "html.parser")
        all_divs = subpage_soup.find_all("div")

        for div in all_divs:
            try:
                price_class = div.get("class")
                if "gl-price-item--crossed" == price_class[1]:
                    if len(prices) < 2:
                        prices.append(div.string)
                if "gl-price-item--sale" == price_class[1]:
                    if len(prices) < 2:
                        prices.append(div.string)
                        products_name = subpage_soup.find(
                            "h1", class_="name___120FN"
                        ).string

                        sales_a_tag = "https://www.adidas.de/" + a_tag["href"]
                        for i in range(4):
                            images = subpage_soup.find_all(
                                "div", class_="content___3m-ue"
                            )
                            all_images.append(images[i].find("img")["src"])
            except:
                pass

        asset = {
            "product_name": products_name,
            "product_link": sales_a_tag,
            "product_image": all_images,
            "product_special_price": prices[SPEACIAL_PRICE],
            "product_price": prices[REGULAR_PRICE],
        }

        return asset
