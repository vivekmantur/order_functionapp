import json
import logging
from datetime import datetime

import azure.functions as func

from config import ORDERS_FILE


def parse_quantity(value):
    if isinstance(value, bool):
        raise ValueError

    if isinstance(value, int):
        return value

    if isinstance(value, str) and value.strip().isdigit():
        return int(value)

    raise ValueError


def parse_price(value):
    if isinstance(value, bool):
        raise ValueError

    if isinstance(value, (int, float)):
        return value

    if isinstance(value, str):
        return float(value)

    raise ValueError


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing Order Request")

    try:
        req_body = req.get_json()

        customer_name = req_body.get("customer_name")
        product_name = req_body.get("product_name")
        quantity = req_body.get("quantity")
        price = req_body.get("price")

        try:
            quantity = parse_quantity(quantity)
        except (TypeError, ValueError):
            return func.HttpResponse(
                "Quantity must be a valid integer",
                status_code=400,
            )

        try:
            price = parse_price(price)
        except (TypeError, ValueError):
            return func.HttpResponse(
                "Price must be a valid integer or float",
                status_code=400,
            )

        order = {
            "customer_name": customer_name,
            "product_name": product_name,
            "quantity": quantity,
            "price": price,
            "timestamp": datetime.utcnow().isoformat(),
            "summary_generated": False,
        }

        with open(ORDERS_FILE, "r", encoding="utf-8") as file:
            orders = json.load(file)

        orders.append(order)

        with open(ORDERS_FILE, "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4)

        response = {
            "message": "Order Saved Successfully",
            "order": order,
        }

        return func.HttpResponse(
            json.dumps(response),
            mimetype="application/json",
            status_code=200,
        )

    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=500,
        )
