import json
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
from selenium import webdriver




class AmazonKraken:
    headers = { 
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
			"accept-encoding": "gzip, deflate, br", 
			"accept-language": "en", 
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36", 
		}

    def get_amazon_products(self):
        urls = [
             "https://www.amazon.com/s?k=boxing+equipment+for+adults&rh=p_n_deal_type%3A23566065011&dc&qid=1684608896&rnid=23566063011&ref=sr_nr_p_n_deal_type_1&ds=v1%3A4RJ79ikbAk7AgG97dOGFHImfUy7Uv%2Bgb5n3hld6IW1Y",
             "https://www.amazon.com/s?k=boxing+equipment+for+adults&rh=p_n_deal_type%3A23566065011&dc&page=2&qid=1684608905&rnid=23566063011&ref=sr_pg_2"
        ]
        productsList = []
        for url in urls:
            response = requests.get(url, headers=self.headers)
            print(response)
            soup = BeautifulSoup(response.content, "html.parser")
           

            all_items = soup.find_all("div", class_="a-section a-spacing-base")
    
            
            """ all_names = soup.find_all(
                "span", class_="a-size-base-plus a-color-base a-text-normal"
            )
            all_a_tags = soup.find_all(
                "a",
                class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal",
            ) """
            #prices = soup.find_all("span", class_="a-offscreen")
            
            """ for i in range(0, len(prices) - 1, 2):
                special_and_regular.append([prices[i].string, prices[i + 1].string]) """
            try:
                for item in all_items:
                    prices = item.find_all("span", class_="a-offscreen")
                    if len(prices) > 1:
                        special_price, price = self.__order_prices([prices[0].string, prices[1].string])
                        product = {
                                "product_name": item.find("span", class_="a-size-base-plus a-color-base a-text-normal").string,
                                "product_link": "https://www.amazon.com/" + item.find("a",class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")["href"],
                                "product_image": self.__get_amazon_images("https://www.amazon.com/" + item.find("a",class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")["href"]),
                                "product_special_price": special_price,
                                "product_price": price
                            }
                        productsList.append(product) 
            except:
                pass
            return productsList
        



    def __order_prices(self, list):
        price = 0.0
        discount_price = 0.0
        if float(list[0][1:]) > float(list[1][1:]):
            price = list[0]
            discount_price = list[1]
        else:
            price = list[1]
            discount_price = list[0]
        return discount_price,  price    
                    


    def __get_amazon_images(self, url):
        print(url)
        all_image_urls = []
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, "html.parser")
        all_images = soup.find_all("div", {"class": "image-size-wrapper fp-image-wrapper"})

        for i in range(len(all_images)):
            if(i > 4):
                break
            url = all_images[i].find("img")["src"]
            print(url)
            all_image_urls.append(url)
        return all_image_urls

            
    

kraken = AmazonKraken()
products = kraken.get_amazon_products()
with open("../productList.json", "w") as outfile:
        json.dump(products, outfile)