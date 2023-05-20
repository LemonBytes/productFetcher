from typing import List
from bs4 import BeautifulSoup
import requests


class EverlastKraken:
    def get_everlast_products():
        everlast_page = requests.get("https://www.everlast.com/deals/sale")
        soup = BeautifulSoup(everlast_page.content, "html.parser")
        all_a_tags = soup.find_all("a", class_="product-item-link")
        prices = soup.find_all("span", class_="price")
        special_and_regular = []
        for i in range(0, len(prices) - 1, 2):
            special_and_regular.append([prices[i].string, prices[i + 1].string])
        productsList = []

        for i in range(len(all_a_tags)):
            product = {
                "product_name": all_a_tags[i].find_next("span").string,
                "product_link": all_a_tags[i]["href"],
                "product_image": __get_everlast_images(all_a_tags[i]["href"]),
                "product_special_price": special_and_regular[i][0],
                "product_price": special_and_regular[i][1],
            }
            productsList.append(product)
        return productsList


def __get_everlast_images(a_tag) -> List[str]:
    images = []
    everlast_subpage = requests.get(a_tag)
    subpage_soup = BeautifulSoup(everlast_subpage.content, "html.parser")
    all_images = subpage_soup.find_all("a", {"class": "product-image"}).find(
        "img", recursive=False
    )
    for image in all_images:
        images.append(image["src"])
    return images
