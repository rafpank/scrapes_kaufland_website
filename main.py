import requests
import click
from lxml.html import fromstring
"""
Usage:
    python M05L20.py <URL><CATEGORY_XPATH>
Prints selected product information from the given website.    
"""

# URL = 'https://sklep.kaufland.pl/oferta/przeglad.html?kloffer-week=current&kloffer-category=01_Mi%C4%99so__Dr%C3%B3b__W%C4%99dliny"'
# CATEGORY_XPATH = '//*[@id="cat_0002_K-Card"]/div[2]/div/div'

def page_downloading (url):
    """
    Downloanding the HTML content from given url

    :param url: str - The URL of the website to dowland
    :return : str - The HTML content of the website as plain text
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    response = requests.get(url, headers=headers)
    
    return response.text


def product_list_finding(url, category_xpath):
    """
    Extracts a list of products from a website using the specified XPath.

    :param url: str - The URL of the website to scrape.
    :param cathegory_xpath: str - The XPath for the product category container.
    :return: list - A list of elements corresponding to products, or an empty list if no products are found.
    """
    dom = fromstring(page_downloading(url))
    try: 
        products = dom.xpath(category_xpath)  
        if not products:
            print('Nie znaleziono produktów dla podanej kategorii')
            return []
        
    except Exception as e:
        print(f'Niepoprawny XPath: {e}')
        return
    
    return products


def extracting_products_details (product):
    """
    Extracts details about a single product from its HTML structure.

    :param product: lxml.html.HtmlElement - The HTML element containing product details.
    :return: dict - A dictionary containing product details:
        - 'producer': The producer's name, or "Brak producenta" if not found.
        - 'name': The product name, or "Brak nazwy" if not found.
        - 'weight': The product weight, or "Brak wagi" if not found.
        - 'price': The product price, or "Brak ceny" if not found.
    """
    producer = product.xpath('.//div[1]/div[4]/div[1]/text()')  
    name = product.xpath('.//div[1]/div[4]/div[2]/text()')      
    weight = product.xpath('.//div[1]/div[4]/div[3]/text()')
    price_per_kg = product.xpath('.//div[1]/div[4]/div[4]/text()')     
    alternative_price = product.xpath('.//div[2]/div/div/div[2]/text()')  

    price = alternative_price[0].strip() if alternative_price else (price_per_kg[0].strip() if price_per_kg else "Brak ceny")
    
    return {
        'producer' : producer[0].strip() if producer else 'Brak producenta',
        'name' : name[0].strip() if name else 'Brak nazwy',
        'weight' : weight[0].strip() if weight else 'Brak wagi',
        'price' : price
    }

def product_list_assembling(products):
    """
    Creates a list of dictionaries with product details.

    :param products: list - A list of HTML elements representing products.
    :return: list - A list of dictionaries, each containing details about a product.
    """
    product_details = []
    for product in products:
        details = extracting_products_details(product)
        product_details.append(details)
    return product_details
    

@click.command()
@click.argument('url')
@click.argument('category_xpath')


def main(url, category_xpath):
    products = product_list_finding(url, category_xpath)
    product_details = product_list_assembling(products)
    for product in product_details:
        print(f"Producent: {product['producer']}, Nazwa: {product['name']}, Cena: {product['price']}, Gramatura: {product['weight']}")


if __name__ == '__main__':
    main()
