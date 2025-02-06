import re
import logging
from datetime import datetime
import locale
import requests
import json
import numpy as np
from bs4 import BeautifulSoup
import logging 
import re
from string import ascii_letters
import os
from datetime import datetime
import locale


def fetch_html(url):
    """ Fetch and parse the webpage content with enhanced error handling. """
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred while fetching {self.url}: {http_err}")
    return None

def extract_dates(url):
    soup = fetch_html(url)
    if not soup:
        logging.error("Failed to fetch HTML content.")
        return None

    full_text = soup.get_text(" ")  # Extract text with spaces
    date_pattern = r"(\d{1,2} [a-zA-Zéû]+ \d{4})"

    def extract_value(pattern, text, group=1):
        """Utility function to extract a regex match."""
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(group).strip() if match else None

    def parse_date(date_str):
        """Convert French date format to 'DD-MM-YYYY'."""
        try:
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
            return datetime.strptime(date_str, "%d %B %Y").strftime("%d-%m-%Y")
        except ValueError:
            return None

    contract_duration = extract_value(r"Durée\s*du\s*contrat\s*:\s*(\d+\s*mois)", full_text)
    hiring_date = parse_date(extract_value(r"Date\s*d['’]embauche\s*prévue\s*:\s*" + date_pattern, full_text))
    deadline = parse_date(extract_value(r"Date\s*Limite\s*Candidature\s*:\s*\w+\s*" + date_pattern, full_text))
    
    print("contract_duration:", contract_duration)
    return {
        'contract_duration': contract_duration,
        'hiring_date': hiring_date,
        'deadline': deadline
    }


session = requests.Session() 
url = "https://emploi.cnrs.fr/Offres/CDD/UMR9213-MATGUI0-013/Default.aspx"
print(extract_dates(url))