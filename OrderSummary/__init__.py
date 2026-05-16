import json
import logging
from datetime import datetime, timedelta

import azure.functions as func

from config import ORDERS_FILE, SUMMARY_FILE, SUMMARY_WINDOW_MINUTES


def main(mytimer: func.TimerRequest) -> None:
    logging.info("Generating Order Summary")

    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as file:
            orders = json.load(file)

        now = datetime.utcnow()
        period_start = now - timedelta(minutes=SUMMARY_WINDOW_MINUTES)

        filtered_orders = []

        for order in orders:
            order_time = datetime.fromisoformat(
                order["timestamp"],
            )

            if order_time >= period_start and not order.get("summary_generated", False):
                filtered_orders.append(order)

        total_orders = len(filtered_orders)

        total_revenue = sum(
            order["quantity"] * order["price"]
            for order in filtered_orders
        )

        unique_products = list(
            set(
                order["product_name"]
                for order in filtered_orders
            )
        )

        large_orders = [
            order for order in filtered_orders
            if order["quantity"] > 5
        ]

        summary = {
            "generated_at": now.isoformat(),
            "period_start": period_start.isoformat(),
            "period_end": now.isoformat(),
            "summary_window_minutes": SUMMARY_WINDOW_MINUTES,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "unique_products": unique_products,
            "large_orders": large_orders,
        }

        with open(SUMMARY_FILE, "r", encoding="utf-8") as file:
            summaries = json.load(file)

        summaries.append(summary)

        with open(SUMMARY_FILE, "w", encoding="utf-8") as file:
            json.dump(summaries, file, indent=4)

        for order in filtered_orders:
            order["summary_generated"] = True
            order["summary_generated_at"] = now.isoformat()

        with open(ORDERS_FILE, "w", encoding="utf-8") as file:
            json.dump(orders, file, indent=4)

        print("\n===== ORDER SUMMARY =====")
        print(json.dumps(summary, indent=4))

    except Exception as e:
        logging.error(str(e))
