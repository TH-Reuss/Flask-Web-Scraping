import json


class Product:
    def __init__(self, title, price, url, image_url):
        self.title = title
        self.description = ""
        self.price = price
        self.url = url
        self.image_url = image_url

    def to_json(self):
        return json.dumps(self.__dict__)
