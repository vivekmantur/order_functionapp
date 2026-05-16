import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")

SUMMARY_FILE = os.path.join(DATA_DIR, "summary.json")

SUMMARY_WINDOW_MINUTES = 5