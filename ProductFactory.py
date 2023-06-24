from multiprocessing import Pool, Manager
import json
import threading
from kraken.AdidasKraken import AdidasKraken
from kraken.AmazonKraken import AmazonKraken
from kraken.EverlastKraken import EverlastKraken
from kraken.VenumKraken import VenumKraken

class ProductFactory:
    def __init__(self):
        self.products = {
            "amazon": [],
            "everlast": [],
            "adidas": [],

        }
        self.lock = threading.Lock()

    def collect_all_products(self):
        threads = []
        brands = ["everlast", "amazon", "adidas"]

        for brand in brands:
            thread = threading.Thread(target=self.get_products, args=(brand,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        with open("./productList.json", "w") as outfile:
            json.dump(self.products, outfile)

    def get_products(self, brand):
        if brand == "everlast":
            everlast_kraken = EverlastKraken()
            everlast_products = everlast_kraken.get_everlast_products()
            self.__write_to_json(brand=brand, products=everlast_products)
            with self.lock:
                self.products[brand] = everlast_products
        
        elif brand == "amazon":
            amazon_kraken = AmazonKraken()
            amazon_products = amazon_kraken.get_amazon_products()
            self.__write_to_json(brand=brand, products=amazon_products)
            with self.lock:
                self.products[brand] = amazon_products
        
        elif brand == "adidas":
            adidas_kraken = AdidasKraken()
            adidas_products = adidas_kraken.get_adidas_products()
            self.__write_to_json(brand=brand, products=adidas_products)
            with self.lock:
                self.products[brand] = adidas_products
         
        elif brand == "venum":
            venum_kraken = VenumKraken()
            venum_products = venum_kraken.get_venum_products()
            self.__write_to_json(brand=brand, products=venum_products)
            with self.lock:
                self.products[brand] = venum_products

    def __write_to_json(self, brand, products):
        with open(f"./{brand}_products.json", "w") as outfile:
            json.dump(products, outfile)