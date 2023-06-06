from configparser import ConfigParser
import asyncio
import aiohttp
import requests
import os

from bs4 import BeautifulSoup

from utils.utils import fetch
from .product import Product


class FalabellaScrapper:
    def __init__(self, product_name):
        self.product_name = product_name
        self.product_quantity = 0
        self.quantity_pages = 0
        self.products = list()
        self.search_url = "https://www.falabella.com/falabella-cl/search?Ntt={}&page={}"

        config = ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), "scraper_config.ini"))
        self.limit_quantity_page = config.getint("Scraper", "limit_quantity_page")

    async def search_products_concurrent(self):
        self.search_quantity_page()
        tasks = [self.scrape_products(page + 1) for page in range(self.quantity_pages)]
        await asyncio.gather(*tasks)
        self.product_quantity = len(self.products)

    def search_quantity_page(self):
        response = requests.get(self.search_url.format(self.product_name, 1))
        soup = BeautifulSoup(response.content, "html.parser")
        pagination = soup.find_all("button", {"class": "pagination-button-mkp"})

        try:
            self.quantity_pages = int(pagination[-1:][0].get_text())
        except:
            self.quantity_pages = 1

        self.quantity_pages = min(self.quantity_pages, self.limit_quantity_page)

    async def scrape_products(self, page):
        url = self.search_url.format(self.product_name, page)

        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url)
            soup = BeautifulSoup(html, "html.parser")
            product_divs = soup.find_all("div", {"class": "pod"})
            for product_div in product_divs:
                product_title = product_div.find(
                    "b", {"class": "pod-subTitle"}
                ).getText()

                product_price = (
                    product_div.find("a", {"class": "pod-summary"})
                    .find("span")
                    .getText()
                )

                product_url = product_div.find("a", class_="layout_grid-view")["href"]
                product_image = product_div.find("img")
                product_image_url = product_image["src"] if product_image else None

                self.products.append(
                    Product(
                        product_title, product_price, product_url, product_image_url
                    )
                )

    def save_products_to_json(self, filename):
        with open(filename, "w") as file:
            for product in self.products:
                file.write(product.to_json() + ",\n")
