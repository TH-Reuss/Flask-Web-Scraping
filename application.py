from flask import Flask, jsonify, request, make_response, abort
from flask_cors import CORS

from bs4 import BeautifulSoup

from scrapers.falabellaScraper import FalabellaScrapper


application = Flask(__name__)
# Just to EB AWS

CORS(application)


@application.errorhandler(404)
def page_not_found(error):
    # Aquí puedes personalizar la página de error 404
    return "Lamentablemente esta pagina no se encuentra disponible"

@application.route("/products/<string:product_name>", methods=["GET"])
async def getProducts(product_name):
    try:
        falabella = FalabellaScrapper(product_name)
        await falabella.search_products_concurrent()
        serialized_products = [product.__dict__ for product in falabella.products]

        if len(serialized_products) == 0:
            return (
                jsonify({"message": "El producto no se encontró", "status": 404}),
                404,
            )

        return jsonify(serialized_products)

    except:
        return (
            jsonify(
                {
                    "message": "Este producto en especifico presenta problemas, por favor intenta con otro. Mientras mas específica la busqueda mejor.",
                    "status": 500,
                }
            ),
            500,
        )


if __name__ == "__main__":
    application.debug = True
    application.run()