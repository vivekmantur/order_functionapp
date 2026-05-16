import os


BASE_DIR = os.getcwd()
DATA_DIR = os.path.join(BASE_DIR, "data")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
SUMMARY_FILE = os.path.join(DATA_DIR, "summary.json")
SUMMARY_WINDOW_MINUTES = 5
