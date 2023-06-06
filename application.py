from flask import Flask, jsonify, request, make_response, abort
from flask_cors import CORS

from bs4 import BeautifulSoup
import uuid

from scrapers.falabellaScraper import FalabellaScrapper


application = Flask(__name__)

CORS(application)


@application.errorhandler(404)
def page_not_found(error):
    return "Lamentablemente esta pagina no se encuentra disponible"

@application.route("/products/<string:product_name>", methods=["GET"])
async def getProducts(product_name):
    try:
        falabella = FalabellaScrapper(product_name)
        await falabella.search_products_concurrent()
        serialized_products = [product.__dict__ for product in falabella.products]

        for product in serialized_products:
            product["id"] = str(uuid.uuid4())

        if len(serialized_products) == 0:
            response = jsonify({"message": "El producto no se encontró", "status": 404})
            response.headers.add('Content-Type', 'application/json')
            return (response, 404)

        return jsonify(serialized_products)

    except Exception:
        response = jsonify({"message": "Este producto en especifico presenta problemas, por favor intenta con otro. Mientras mas específica la busqueda mejor.","status": 500,})
        response.headers.add('Content-Type', 'application/json')
        return (response, 500)


if __name__ == "__main__":
    application.debug = False
    application.run()
