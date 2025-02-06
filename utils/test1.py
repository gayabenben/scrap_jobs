import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import json
import logging
import os
from datetime import datetime

def load_from_json(filename) -> dict:
    try:
        with open(filename, "r", encoding='utf-8') as file:
            return json.load(file)
    except FileExistsError as e:
        logging.error(f"File {filename} not found.")
        return {}
    

def extract_job_offers(url) -> dict:
    """Extract job offers from a given URL and return them as a dictionary {offer_id: {...}}."""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur: Impossible d'accéder à {url}")
        return {}

    soup = BeautifulSoup(response.text, 'html.parser')
    offers = {}

    base_url = "https://emploi.cnrs.fr" if "cnrs" in url else ""

    for row in soup.select("tbody tr[itemtype='http://schema.org/JobPosting']"):
        date_posted = row.select_one("span[itemprop='datePosted']").text.strip()
        title_element = row.select_one("a[itemprop='url']")
        title = "".join([unquote(s) for s in title_element.text.strip()])
        offer_url = base_url + title_element['href']
        location = row.select("td")[2].text.strip()
        region = row.select("td")[3].text.strip()
        offer_id = offer_url.split("/")[-2]

        dictfile = "job_offers.json"
        # check if the file exists
        
        if os.path.exists(dictfile):
            loaded_offers = load_from_json("job_offers.json")
        else:
            loaded_offers = {}        
        if offer_id in loaded_offers.keys():
            print(f"Offer {offer_id} already exists, skipping.")
            continue
        
        print(f"Found new offer {offer_id}, published on: {date_posted}")

        offers[offer_id] = {
            "date_posted": date_posted,
            "title": title,
            "url": offer_url,
            "location": location,
            "region": region
        }

    # Sort offers by `date_posted` (descending order)
    try:
        offers = dict(sorted(offers.items(), key=lambda x: datetime.strptime(x[1]["date_posted"], "%d/%m/%Y"), reverse=True))
    except ValueError:
        print("Error parsing dates; returning unsorted results.")

    # Save to JSON
    save_to_json(offers, "job_offers.json")

    return offers




def lookup_job_offer(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur: Impossible d'accéder à {url}")
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    job_offer = {}
    
    if "cnrs" in url:
        base_url = "https://emploi.cnrs.fr"
    else:
        base_url = None
    
    return job_offer

def save_to_json(data, filename):
    """ 
    if filename exists, load it and update it with new data 
    """
    if filename:
        mode = "a"
    else:
        mode = "w"
    try:
        with open(filename, mode, encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error: {e}")
    return

if __name__ == "__main__":
    url = "https://emploi.cnrs.fr/Recherche.aspx?bassin=INDEF&type=ITCDD&texte="
    job_offers = extract_job_offers(url)
    
    # get only 4 offers
    job_offers = {k: job_offers[k] for k in list(job_offers)[:2]}
    #print(job_offers.values())
    
    base_url = "https://emploi.cnrs.fr"
    
    url = "https://emploi.cnrs.fr/Offres/CDD/MOY500-CARHUB-012/Default.aspx"
    #find_offer = lookup_job_offer(url)
    #print(find_offer)
    