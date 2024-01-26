# Uptime.py
# Script for checking the uptime of the host at regular intervalls
# © Paul Maier 2024

import requests
import time
import logging

# Configure logging
logging.basicConfig(
    filename="uptime.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def check_internet_connection():
    try:
        # Try to make a simple HTTP request to Cloudflare DNS server (1.1.1.1)
        response = requests.get("http://1.1.1.1", timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.ConnectionError:
        return False

if __name__ == "__main__":
    while True:
        if check_internet_connection():
            logging.info("Internet connection is active.")
        else:
            logging.warning("No internet connection.")

        # Wait for one minute before checking again
        time.sleep(60)
