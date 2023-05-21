import json
from random import choice
from time import sleep
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.by import By



class AmazonKraken:
    def get_amazon_products(self):
        urls = [
             "https://www.amazon.com/s?k=boxing+equipment+for+adults&rh=p_n_deal_type%3A23566065011&dc&crid=OTTZZGNREI57&qid=1684682255&rnid=23566063011&sprefix=boxing+equipment+for+adults%2Caps%2C170&ref=sr_nr_p_n_deal_type_1&ds=v1%3Ajkdt5h1%2FhqH0oFSNhZPJGS4awqKWkMMvOoF8oMrMm%2B0",
             "https://www.amazon.com/s?k=boxing+equipment+for+adults&rh=p_n_deal_type%3A23566065011&dc&page=2&crid=OTTZZGNREI57&qid=1684682272&rnid=23566063011&sprefix=boxing+equipment+for+adults%2Caps%2C170&ref=sr_pg_2"
        ]
        productsList = []
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("window-size=1400,1200")
        #options.add_argument(f'--user-agent={self.__get_random_proxy()}')
        options.add_argument(f'--user-agent={self.__get_random_useragent()}')
        browser = webdriver.Chrome(options=options)
        for url in urls:
            print(url)
            browser.get(url)
            html_source = browser.page_source
            soup = BeautifulSoup(html_source, "html.parser")
            all_items = soup.find_all("div", class_="a-section a-spacing-base")

            for item in all_items:
                prices = item.find_all("span", class_="a-offscreen")
                if len(prices) > 1:
                    special_price, price = self.__order_prices(prices[0].string, prices[1].string)
                    product_url = "https://www.amazon.com/" + item.find("a",class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")["href"]
                    name =  item.find("span", class_="a-size-base-plus a-color-base a-text-normal").string,
                    images =  self.__get_amazon_images(url = product_url, browser=browser)
                    product = {
                            "product_name": name,
                            "product_link": product_url,
                            "product_image": images,
                            "product_special_price": special_price,
                            "product_price": price
                        }
                    productsList.append(product) 
           
        return productsList

    def read_file(self, filename, method):
        with open(filename, method) as f:
            content = [line.strip('\n') for line in f]
            return content    

    def __get_random_useragent(self):
        useragents = self.read_file('./useragents.txt', 'r')
        return choice(useragents)
    
    def __get_random_proxy(self):
        proxies_file = self.read_file('../streaming_http_proxies.txt', 'r')

    def __order_prices(self, price_one, price_two):
        price = 0.0
        discount_price = 0.0
        if(float(float(price_one.replace('$', '').replace(',', ''))) > float(price_two.replace('$', '').replace(',', ''))):
            price = price_one
            discount_price = price_two
        else:
            price = price_two
            discount_price = price_one
        return discount_price.strip(),  price.strip()    
                    


    def __get_amazon_images(self, url, browser):
        browser.get(url)
        self.__load_images(browser=browser)
        all_image_urls = []
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, "html.parser")
        all_images = soup.find_all("div", {"class": "imgTagWrapper"})
        print(all_images)
        
        for i in range(len(all_images)):
            if i > 5:
                break
            url = all_images[i].find(
            "img",  recursive=False
            )
            if url == None:
                continue
            all_image_urls.append(url["src"])

        return all_image_urls


    def __load_images(self, browser):
        for i in range(1, 20, 1):
            try:
                icons = browser.find_element(By.XPATH, f"/html/body/div[1]/div[2]/div[9]/div[3]/div[3]/div[1]/div[1]/div/div/div[1]/ul/li[{i}]/span/span/span/input")
                browser.execute_script("arguments[0].click();", icons)
            except:
                continue
            sleep(1)
                                        



    

