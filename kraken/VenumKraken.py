from bs4 import BeautifulSoup
from pyparsing import List
import requests
from requests_html import HTMLSession
import json


class VenumKraken:
    payload = {}
    headers = {
            "authority": "euro.venum.com",
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "de,en;q=0.9",
            "cookie": "mage-banners-cache-storage=%7B%7D; store=en; _ga=GA1.2.808143475.1680440698; _fbp=fb.1.1680440697919.1664704544; _tt_enable_cookie=1; _ttp=Qhj4p8S78pjxz2OqLuzbANwuzYr; _ga=GA1.3.808143475.1680440698; PHPSESSID=5fvtbvlenv3pqmj40n7gb8jtih; X-Magento-Vary=79d42edc27c19a90f9cb2ddc07623b7a62aa7718; _gid=GA1.2.719610533.1684496724; form_key=FOqZp9QbS0iCryys; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; private_content_version=9ac85900c467afad109f027f5929c40f; _gid=GA1.3.719610533.1684496724; mage-cache-sessid=true; mage-messages=; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; section_data_ids=%7B%22company%22%3A1684496358%7D; user_allowed_save_cookie=%7B%223%22%3A1%7D; _gat_gtag_UA_97164781_1=1; __kla_id=eyIkcmVmZXJyZXIiOnsidHMiOjE2ODA0NDA2OTgsInZhbHVlIjoiaHR0cDovL2xvY2FsaG9zdDozMDAwLyIsImZpcnN0X3BhZ2UiOiJodHRwczovL2V1cm8udmVudW0uY29tL2VuL2NhdGFsb2cvcHJvZHVjdC92aWV3L2lkLzgxNTAxL2NhdGVnb3J5LzE1ODcvIn0sIiRsYXN0X3JlZmVycmVyIjp7InRzIjoxNjg0NTgyNDEzLCJ2YWx1ZSI6IiIsImZpcnN0X3BhZ2UiOiJodHRwczovL2V1cm8udmVudW0uY29tL2VuL3Byb21vLmh0bWwifX0=; _gat=1",
            "referer": "https://euro.venum.com/en/promo.html",
            "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
    }
     

    def get_venum_products(self):
        productsList = []
        for i in range(1, 7, 1):
            response = requests.request(
                "GET",
                url=f"https://euro.venum.com/en/promo.html?p={i}&is_scroll=1",
            ).text
            soup = BeautifulSoup(response, "html.parser")
            print(i)
            all_a_tags = soup.find_all("a", class_="product-item-link")
            prices = soup.find_all("span", class_="price")
            avaiable_divs = soup.find_all("div", class_="uncover-swatch-group")
            special_and_regular = []
            for i in range(0, len(prices) - 1, 2):
                special_and_regular.append([prices[i].string, prices[i + 1].string])

            for i in range(len(special_and_regular)):
                not_avaiable = avaiable_divs[i].find("div", class_="stock unavailable")
                if not_avaiable:
                    print("not avaiable")
                else: 
                    product = {
                        "product_name": all_a_tags[i].string,
                        "product_link": all_a_tags[i]["href"],
                        "product_image": self.__get_venum_images(url=all_a_tags[i]["href"]),
                        "product_special_price": special_and_regular[i][1],
                        "product_price": special_and_regular[i][0],
                    }
                    productsList.append(product)
        return productsList

    def __get_venum_images(self, url):
        all_image_urls = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        all_images = soup.find_all("img", class_="product-image")
        for i in range(len(all_images)):
            if(i > 4):
                break
            all_image_urls.append(all_images[i]["src"])
        return all_image_urls

       

