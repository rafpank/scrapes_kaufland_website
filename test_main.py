# Calling from the command prompt
# $ pytest -v .\test_main.py   

from lxml.html import fromstring
from M05L20 import page_downloading, product_list_finding, extracting_products_details, product_list_assembling

CATEGORY_XPATH = '//div[@class="product"]'
HTML_CONTENT = """
<div>
    <div class="product">
        <div>Producent A</div>
        <div>Nazwa Producktu A</div>
        <div>500 g</div>
        <div>9,99 zł</div>
    </div>
    <div class="product">
        <div>Producent B</div>
        <div>Nazwa produktu B</div>
        <div>1 kg</div>
        <div>19,99 zł</div>
    </div>
</div>
"""

def test_page_downloading():
    url = "https://sklep.kaufland.pl/oferta/przeglad.html?kloffer-week=current"
    html = page_downloading(url)
    assert len(html) > 0, 'Treść strony nie została załadowana'


def test_product_list_finding_valid_xpath():
    dom = fromstring(HTML_CONTENT)
    products = dom.xpath(CATEGORY_XPATH)
    assert len(products) == 2, "Should find 2 products"
    assert products[0].xpath('.//div[1]/text()')[0] == "Producent A"
    assert products[1].xpath('.//div[1]/text()')[0] == "Producent B"


def test_product_list_finding_invalid_xpath():
    dom = fromstring(HTML_CONTENT)
    invalid_xpath = '//div[@class="invalid"]'
    prodcts =dom.xpath(invalid_xpath)
    assert len(prodcts) == 0, "Should find no products for invalid XPath"




def test_extracting_products_details_empty():
    dom = fromstring("<div></div>")
    products = dom
    details = extracting_products_details(products)
    assert details['producer'] == "Brak producenta"
    assert details['name'] == "Brak nazwy"
    assert details['weight'] == "Brak wagi"
    assert details['price'] == "Brak ceny"
