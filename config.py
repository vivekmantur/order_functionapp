import os

DATA_DIR = "/tmp/data"

os.makedirs(DATA_DIR, exist_ok=True)

ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
SUMMARY_FILE = os.path.join(DATA_DIR, "summary.json")

SUMMARY_WINDOW_MINUTES = 5
