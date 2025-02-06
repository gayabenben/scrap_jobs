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

    full_text = soup.get_text(" ")  # Get all text with spaces between elements
    print(full_text)  # Debug: Check the text content

    contract_duration = None
    hiring_date = None
    deadline = None

    # Regex for dates (e.g., "25 janvier 2024")
    date_pattern = r"(\d{1,2} [a-zA-Zéû]+ \d{4})"

    # Search for contract duration
    contract_match = re.search(r"Durée\s*du\s*contrat\s*:\s*(\d+\s*mois)", full_text, re.IGNORECASE)
    print(contract_match[0])
    if contract_match:
        contract_duration = contract_match.group(1).strip()
        print(contract_duration)

    # Search for hiring date
    hiring_match = re.search(r"Date\s*d['’]embauche\s*prévue\s*:\s*" + date_pattern, full_text, re.IGNORECASE)
    if hiring_match:
        hiring_date_str = hiring_match.group(1)
        print(hiring_date_str)
        try:
            locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
            hiring_date = datetime.strptime(hiring_date_str, "%d %B %Y").strftime("%d-%m-%Y")
            print(hiring_date)
        except ValueError:
            hiring_date = None
    # Search for application deadline (more flexible regex)
    deadline_match = re.search(r"Date\s*Limite\s*Candidature\s*:\s*\w+\s*(\d{1,2} [a-zA-Zéû]+ \d{4})", full_text, re.IGNORECASE)
    #print(deadline_match)
    if deadline_match:
        deadline_str = deadline_match.group(1)
        deadline = re.search(r"(\d{1,2} [a-zA-Zéû]+ \d{4})", deadline_str)
        #print(deadline[0])
        deadline_str = deadline.group(1)
        try:
            deadline = datetime.strptime(deadline_str, "%d %B %Y").strftime("%d-%m-%Y")
            print(deadline)
        except ValueError as e:
            print(f"Error parsing deadline: {e}")
            deadline = None

    # Search for application deadline
    

    return {
        'contract_duration': contract_duration,
        'hiring_date': hiring_date,
        'deadline': deadline
    }
    
session = requests.Session() 
url = "https://emploi.cnrs.fr/Offres/CDD/UMR9213-MATGUI0-013/Default.aspx"
extract_dates(url)