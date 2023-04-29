from bs4 import BeautifulSoup
import requests 
from requests_html import HTMLSession
import json



def get_venum_products():
    venumPage = requests.get("https://euro.venum.com/en/promo.html")
    soup = BeautifulSoup(venumPage.content, 'html.parser')
    all_a_tags = soup.find_all('a', class_="product-item-link")
    all_images = soup.find_all('img', class_="product-image-photo")
    prices = soup.find_all('span', class_="price")
    special_and_regular = []
    for i in range(0, len(prices) -1, 2 ):
         special_and_regular.append([prices[i].string, prices[i+1].string])
    productsList = []
    for i in range(len(all_a_tags)):
        product = {
            "product_name" : all_a_tags[i].string,
            "product_link" :  all_a_tags[i]['href'],
            "product_image" : all_images[i]['src'],
            "product_special_price" : special_and_regular[i][1],
            "product_price" : special_and_regular[i][0]
        }
        productsList.append(product)
    return productsList
   

def get_everlast_products():
    everlast_page = requests.get("https://www.everlast.com/deals/sale")
    soup = BeautifulSoup(everlast_page.content, 'html.parser')
    all_a_tags = soup.find_all('a', class_="product-item-link")
    all_images = soup.find_all('img', class_="product-image-photo")
    prices = soup.find_all('span', class_="price")
    special_and_regular = []
    for i in range(0, len(prices) -1, 2 ):
         special_and_regular.append([prices[i].string, prices[i+1].string])
    productsList = []
    for i in range(len(all_a_tags)):
        product = {
            "product_name" : all_a_tags[i].find_next("span").string,
            "product_link" :  all_a_tags[i]['href'],
            "product_image" : all_images[i]['src'],
            "product_special_price" : special_and_regular[i][0],
            "product_price" : special_and_regular[i][1]
        }
        productsList.append(product)
    return productsList

def get_sub_pages(a_tags, headers):
        sales_a_tags = []
        all_images = []
        products_names = []
        products_prices = []
        for a in a_tags:
            sub_page = requests.get("https://www.adidas.de/" + a["href"], headers=headers)
            sub_soup = BeautifulSoup(sub_page.content, 'html.parser')
            all_divs = sub_soup.find_all("div")
            prices = []
          
            images_src = []
           
            for div in all_divs:
                try:
                    price_class = div.get("class")
                    if "gl-price-item--crossed" == price_class[1]:
                        if len(prices) < 2:
                            prices.append(div.string)
                    if "gl-price-item--sale" == price_class[1]:
                            if len(prices) < 2:
                                prices.append(div.string)
                                products_prices.append(prices)
                                products_names.append(sub_soup.find("h1", class_="name___120FN").string)
                                sales_a_tags.append("https://www.adidas.de/" + a["href"]) 
                                for i in range(4):
                                    images = sub_soup.find_all("div", class_="content___3m-ue")
                                    images_src.append(images[i].find("img")["src"])
                                all_images.append(images_src)   
                except:
                    pass 
        assets = {
            "product_name" : products_names,
            "product_link" : sales_a_tags,
            "product_image" : all_images,
            "product_price" : products_prices
        }
        return assets    
  
def get_adidas_products():
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    adidas_page = requests.get("https://www.adidas.de/en/boxing", headers=headers)
    soup = BeautifulSoup(adidas_page.content, 'html.parser')
    all_a_tags = soup.find_all("a", class_="glass-product-card__assets-link")
    assets = get_sub_pages(all_a_tags, headers)
    productList = []
    for i in range(len(assets["product_name"])):
        product = {
            "product_name" : assets["product_name"][i],
            "product_link" : assets["product_link"][i],    
            "product_image" : assets["product_image"][i],
            "product_special_price" :  assets["product_price"][i][0],  
            "product_price" :  assets["product_price"][i][1]
        }
        productList.append(product)
    return productList


def get_amazon_products():
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    session = HTMLSession()
    amazon_page = session.get("https://www.amazon.com/s?k=boxing&i=sports-and-fitness&bbn=10971181011&rh=n%3A10971181011%2Cp_n_deal_type%3A23566065011%2Cp_89%3ANike%7CRingside%7CUnder+Armour&dc&language=en_US&ds=v1%3AkLgHmn3LuBepatAFGAtoJCyS%2Fn6DLBPHdgb02YrjJBU&__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=190ZJDSSMA8FB&qid=1671732055&rnid=2528832011&sprefix=boxin%2Csports-and-fitness%2C204&ref=sr_nr_p_89_4", headers=headers)
    amazon_page.html.render()
    soup = BeautifulSoup(amazon_page.html.html, 'html.parser')
    all_names = soup.find_all("span", class_="a-size-base-plus a-color-base a-text-normal")
    all_a_tags = soup.find_all("a", class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
    all_images = soup.find_all("img", class_="s-image")
    prices = soup.find_all("span", class_="a-offscreen")
    special_and_regular = []
    for i in range(0, len(prices) -1, 2 ):
         special_and_regular.append([prices[i].string, prices[i+1].string])

  
    productsList = []
    try:
        for i in range(len(all_a_tags)):
            if "$" not in special_and_regular[i][0]  or "$" not in special_and_regular[i][1]:
                continue
            product = {
                "product_name" : all_names[i].string,
                "product_link" :  "https://www.amazon.com/" + all_a_tags[i]['href'],
                "product_image" : all_images[i]['src'],
                "product_special_price" :   special_and_regular[i][0],
                "product_price" :   special_and_regular[i][1]
            }
            productsList.append(product)    
    except:
        pass    
    return productsList
        

def tie_all_products():
    productList = {
        "venum" :get_venum_products(),
        "adidas" : get_adidas_products(),
        "amazon" : get_amazon_products(),
        "everlast" : get_everlast_products(),
    }
    with open('productList.json', 'w') as outfile:
        json.dump(productList, outfile)
      