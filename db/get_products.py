import requests
import json

def get_products(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json"
    }

    # Hacer la solicitud
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Genera una excepción si el código de estado no es 200
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud a {url}: {e}")
        return []

    # Depuración: imprime el texto de la respuesta
    print(f"Respuesta del servidor para {url}: {response.text[:500]}...")

    # Procesar el JSON
    return parse_products_from_json(response.text)


def parse_products_from_json(json_text):
    try:
        products = json.loads(json_text)
        if not isinstance(products, list):  # Asegúrate de que sea una lista
            print("Error: El JSON no contiene una lista de productos.")
            return []
    except json.JSONDecodeError:
        print("Error: El texto no es un JSON válido.")
        return []

    matrix = []
    for product in products:
        row = [
            product.get("productId", ""),
            product.get("productName", ""),
            product.get("brand", ""),
            _get_price(product),
            _get_price(product, "ListPrice"),
            _get_measurement_unit(product),
            _get_unit_multiplier(product),
            _get_stock(product),
            _get_first_category(product),
            _get_promotions(product),
            _get_payment_methods(product),
            f"https://www.metro.pe{product.get('link', '')}"
        ]
        matrix.append(row)

    return matrix


# --- Funciones auxiliares ---

def _get_payment_methods(product):
    """Obtiene los métodos de pago (ej: Visa, Yape)."""
    if "items" in product and product["items"]:
        sellers = product["items"][0].get("sellers", [])
        if sellers and "commertialOffer" in sellers[0]:
            payment_options = sellers[0]["commertialOffer"].get("PaymentOptions", {})
            if "paymentSystems" in payment_options:
                methods = {m["name"] for m in payment_options["paymentSystems"] if "name" in m}
                return ", ".join(methods) if methods else "No especificado"
    return "No especificado"

def _get_price(product, price_field="Price"):
    """Obtiene el precio (actual o original) del primer seller."""
    if "items" in product and product["items"]:
        sellers = product["items"][0].get("sellers", [])
        if sellers and "commertialOffer" in sellers[0]:
            return sellers[0]["commertialOffer"].get(price_field)
    return ""


def _get_measurement_unit(product):
    """Obtiene la unidad de medida (ej: 'kg')."""
    if "items" in product and product["items"]:
        return product["items"][0].get("measurementUnit", "")
    return ""


def _get_unit_multiplier(product):
    """Obtiene el multiplicador de unidad (ej: 0.16 para 160g)."""
    if "items" in product and product["items"]:
        return product["items"][0].get("unitMultiplier", "")
    return ""


def _get_stock(product):
    """Obtiene el stock disponible."""
    if "items" in product and product["items"]:
        sellers = product["items"][0].get("sellers", [])
        if sellers and "commertialOffer" in sellers[0]:
            return sellers[0]["commertialOffer"].get("AvailableQuantity", "")
    return ""


def _get_first_category(product):
    """Obtiene la primera categoría del producto."""
    categories = product.get("categories", [])
    return categories[0] if categories else ""


def _get_promotions(product):
    """Extrae las 3 principales promociones."""
    promotions = []
    if "clusterHighlights" in product:
        clusters = product["clusterHighlights"].values()
        promotions = [p for p in clusters if "desct" in p.lower()][:3]
    return ", ".join(promotions)
