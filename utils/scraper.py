import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
import logging
import os
from datetime import datetime
from load import Load

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class JobScraper:
    def __init__(self, url: str, json_file="job_offers.json"):
        self.url = url
        self.json_file = json_file
        self.offers = []
        #loader = Load(self.json_file)
        self.loader = Load(json_file)  # Define loader once for all
    
    
    def _load_offers(self):
        """Load offers from a JSON file if exists."""
        if os.path.exists(self.json_file):
            self.offers = self.loader.load_from_json()
        else:
            self.offers = {}

    def _save_offers(self):
        """Save offers to JSON file."""
        self.loader.save_to_json(self.offers)
        

    def _get_base_url(self) -> str:
        """Determine base URL based on the site."""
        return "https://emploi.cnrs.fr" if "cnrs" in self.url else ""

    def _parse_job_row(self, row) -> dict:
        """Parse the job posting row and return details."""
        date_posted = row.select_one("span[itemprop='datePosted']").text.strip()
        title_element = row.select_one("a[itemprop='url']")
        title = "".join([unquote(s) for s in title_element.text.strip()])
        offer_url = self._get_base_url() + title_element['href']
        location = row.select("td")[2].text.strip()
        region = row.select("td")[3].text.strip()
        offer_id = offer_url.split("/")[-2]

        return {
            "offer_id": offer_id,
            "date_posted": date_posted,
            "title": title,
            "url": offer_url,
            "location": location,
            "region": region,
        }

    def extract_job_offers(self):
        """Extract job offers and add them to the dictionary."""
        response = requests.get(self.url)
        if response.status_code != 200:
            logging.error(f"Error: Unable to access {self.url}")
            return {}

        soup = BeautifulSoup(response.text, 'html.parser')
        base_url = self._get_base_url()

        # Ensure previous offers are loaded
        self._load_offers()

        for row in soup.select("tbody tr[itemtype='http://schema.org/JobPosting']"):
            job_details = self._parse_job_row(row)
            offer_id = job_details["offer_id"]

            if offer_id in self.offers:
                logging.info(f"Offer {offer_id} already exists, skipping.")
                continue

            logging.info(f"Found new offer {offer_id}, published on: {job_details['date_posted']}")
            self.offers[offer_id] = job_details

        # Sort offers by `date_posted` (descending order)
        try:
            self.offers = dict(sorted(self.offers.items(), key=lambda x: datetime.strptime(x[1]["date_posted"], "%d/%m/%Y"), reverse=True))
        except ValueError:
            logging.warning("Error parsing dates; returning unsorted results.")

        # Save updated offers
        self._save_offers()

        return self.offers

if __name__ == "__main__":
    url = "https://emploi.cnrs.fr/Offres/CDD/UMR9213-MATGUI0-013/Default.aspx"
    scraper = JobScraper(url)
    scraper.extract_job_offers()