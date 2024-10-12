# scrape.py
import time
import random
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import List, Dict, Optional, Tuple
import csv
import io
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

def fetch_tables(url: str, session: requests.Session, headers: Dict[str, str]) -> Tuple[str, Optional[List[Tag]]]:
    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')
            return url, tables
        else:
            # Fall back to Selenium if requests fails
            # Useful if websites load content dynamically with JavaScript.
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(service=Service(), options=chrome_options)

            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'table'))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tables = soup.find_all('table')
            driver.quit()
            return url, tables
    except requests.RequestException as e:
        print(f"Failed to retrieve {url} with requests: {e}")
        return url, None
    except Exception as e:
        print(f"An error occurred with {url} using Selenium: {e}")
        return url, None

def scrape_single_url(url: str) -> Tuple[Optional[List[str]], Optional[str]]:
    """
    Scrapes a single URL and converts its tables to CSV format.

    Args:
        url (str): The URL to scrape.

    Returns:
        Tuple[Optional[List[str]], Optional[str]]: A list of CSV strings if successful, else an error message.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1'
    }

    session = requests.Session()

    try:
        url_fetched, tables = fetch_tables(url, session, headers)
        if tables is None:
            return None, f"Failed to retrieve tables from {url_fetched}"
        
        csv_tables = convert_tables_to_csv({url_fetched: tables}).get(url_fetched, [])
        if not csv_tables:
            return None, f"No tables found at {url_fetched}"
        
        return csv_tables, None
    except Exception as e:
        return None, str(e)

def get_domain_from_url(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc

def table_to_csv(table: Tag, domain: str) -> str:
    output = io.StringIO()
    writer = csv.writer(output)

    first_row = True
    for row in table.find_all('tr'):
        cols = row.find_all(['td', 'th'])
        row_data = [col.get_text(strip=True) for col in cols]
        if first_row:
            row_data.insert(0, domain)
            first_row = False
        writer.writerow(row_data)

    return output.getvalue()

def convert_tables_to_csv(results: Dict[str, Optional[List[Tag]]]) -> Dict[str, List[str]]:
    csv_results: Dict[str, List[str]] = {}

    for url, tables in results.items():
        if tables is None:
            csv_results[url] = []
            continue

        domain = get_domain_from_url(url)
        csv_tables = []
        for table in tables:
            csv_content = table_to_csv(table, domain)
            csv_tables.append(csv_content)

        csv_results[url] = csv_tables

    return csv_results

# Define module exports
__all__ = ['scrape_single_url']
