import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import json
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)

class JobScraper:
    def __init__(self, filename='job_offers.json', max_offers=None):
        self.filename = filename
        self.max_offers = max_offers
        self.existing_offers = self.load_existing_offers()
        self.new_offers = {}

    def load_existing_offers(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except ValueError as e:
                logging.error(f"Error loading {self.filename}: {str(e)}")
        return {}

    def extract_job_offers(self, *urls):
        for url in urls:
            response = requests.get(url)
            if response.status_code != 200:
                logging.warning(f"Failed to access {url}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            base_url = "https://emploi.cnrs.fr" if "cnrs" in url else ""

            for row in soup.select("tbody tr[itemtype='http://schema.org/JobPosting']"):
                try:
                    title_element = row.select_one("a[itemprop='url']")
                    offer_url = base_url + title_element['href']
                    offer_id = offer_url.split("/")[-2]

                    if offer_id in self.existing_offers:
                        continue

                    self.new_offers[offer_id] = {
                        "date_posted": row.select_one("span[itemprop='datePosted']").text.strip(),
                        "title": unquote(title_element.text.strip()),
                        "url": offer_url,
                        "location": row.select("td")[2].text.strip(),
                        "region": row.select("td")[3].text.strip()
                    }
                    logging.info(f"New offer found: {offer_id}")

                except ValueError as e:
                    logging.error(f"Error parsing offer: {str(e)}")
                    continue

        self.merge_and_save_offers()

    def merge_and_save_offers(self):
        merged_offers = {**self.existing_offers, **self.new_offers}
        try:
            merged_offers = dict(sorted(
                merged_offers.items(),
                key=lambda x: datetime.strptime(x[1]["date_posted"], "%d/%m/%Y"),
                reverse=True
            ))
        except ValueError as e:
            logging.warning(f"Date sorting error: {str(e)}")

        if self.max_offers:
            merged_offers = dict(list(merged_offers.items())[:self.max_offers])

        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(merged_offers, f, indent=4, ensure_ascii=False)
            logging.info(f"Saved {len(self.new_offers)} new offers to {self.filename}")
        except ValueError as e:
            logging.error(f"Error saving data: {str(e)}")

    def lookup_job_offer(self, url, **kwargs):
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            result = {"url": url}
            
            result["title"] = soup.find("h1").text.strip()
            
            if 'extra_fields' in kwargs:
                for field in kwargs['extra_fields']:
                    result[field] = "Extracted value"
                    
            return result
        except ValueError as e:
            logging.error(f"Lookup error: {str(e)}")
            return {}
        
    # find the number of offers saved in the file
    def count_offers(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    offers = json.load(f)
                    return len(offers)
            except ValueError as e:
                logging.error(f"Error loading {self.filename}: {str(e)}")
        return 0    
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract job offers from CNRS/cea website.")
    parser.add_argument("--site", type=str, default="cnrs", help="Website to scrape (cnrs or cea)")
    args = parser.parse_args()
    
    
    if args.site == "cnrs":
        url = "https://emploi.cnrs.fr/Recherche.aspx"
    elif args.site == "cea":
        url = "https://www.emploi.cea.fr/offre-de-emploi/liste-offres.aspx"
        #"https://www.emploi.cea.fr/accueil.aspx?LCID=1036"
    else:
        raise ValueError("Invalid site specified. Use 'cnrs' or 'cea'")
    
    scraper = JobScraper(filename=f"{args.site}_jobs.json", max_offers=1002)
    #url = "https://emploi.cnrs.fr/Recherche.aspx"
    print("Extracting job offers from ...", url)
    scraper.extract_job_offers(url)
    print(f"Total job offers: {scraper.count_offers()}")
    # Example lookup with additional parameters
    #detailed_offer = scraper.lookup_job_offer(
    #    "https://emploi.cnrs.fr/Offres/CDD/MOY500-CARHUB-012/Default.aspx",
    #    extra_fields=["contract_type", "salary"]
    #)
    #print(detailed_offer)