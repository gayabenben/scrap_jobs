import requests
import json
import re
import os
import csv
import logging
import locale
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
#import numpy as np
import statistics

from salary import DigitExtractor

extractor = DigitExtractor()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WebScraper:
    """Handles webpage requests and HTML parsing."""
    session = requests.Session()

    @staticmethod
    def fetch_html(url):
        try:
            response = WebScraper.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            return None

class JobOffer:
    """Represents a job offer and extracts relevant details."""
    def __init__(self, url):
        self.url = url
        self.title = None
        self.location = None
        self.description = None
        self.contract_type = None
        self.salary = None
        self.salary_mean = 0
        self.education = None
        self.experience = None
        self.industry = None
        self.skills = None
        self.posted_date = None
        self.contract_duration = None
        self.hiring_date = None
        self.deadline = None

    def extract_text(self, soup, selector):
        element = soup.select_one(f'span[itemprop="{selector}"]')
        return element.text.strip() if element else None

    def extract_offer(self):
        soup = WebScraper.fetch_html(self.url)
        if not soup:
            return None
        
        full_text = soup.get_text(" ")
        if "L’offre d’emploi demandée n’existe plus" in full_text:
            logging.warning(f"Offer {self.url} no longer exists.")
            return None
        
        self.title = self.extract_text(soup, 'title')
        self.location = self.extract_text(soup, 'addressLocality')
        self.description = self.extract_text(soup, 'description')
        self.contract_type = self.extract_text(soup, 'employmentType')
        self.salary = extractor.extract_numbers(full_text) 
        print("Salary:", self.salary, self.url)
        #(soup, 'baseSalary') or "0"
        self.salary_mean = self.salary #self.get_salary()
        self.education = self.extract_text(soup, 'educationRequirements')
        self.experience = self.extract_text(soup, 'experienceRequirements')
        self.industry = self.extract_text(soup, 'industry')
        self.skills = self.extract_text(soup, 'skills')
        self.posted_date = self.extract_text(soup, 'datePosted')
        self.contract_duration, self.hiring_date, self.deadline = self.extract_dates(soup)
        
        self.log_missing_fields()
        logging.debug(f"Extracted offer: {self.__dict__}")
        return self

    
    def extract_dates(self, soup):
        full_text = soup.get_text(" ")
        os.makedirs("txt", exist_ok=True)
        
        file = urlparse(self.url).path.split("/")[-2]
        filename = f"txt/{file or 'unknown'}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(full_text)
            
        def extract_value(pattern, text, group=1):
            """Utility function to extract a regex match."""
            try:
                match = re.search(pattern, text, re.IGNORECASE)
                return match.group(group).strip() if match else None
            except (AttributeError, IndexError) as e:
                logging.error(f"Error extracting value with pattern {pattern}: {e}")
                return None
        
        def parse_date(date_str):
            try:
                locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
                return datetime.strptime(date_str, "%d %B %Y").strftime("%d-%m-%Y")
            except ValueError:
                return None
        
        date_pattern = r"(\d{1,2} [a-zA-Zéû]+ \d{4})"
        
        contract_duration = extract_value(r"Durée\s*du\s*contrat\s*:\s*(\d+\s*mois)", full_text)
        hiring_date = parse_date(extract_value(r"Date\s*d['’]embauche\s*prévue\s*:\s*" + date_pattern, full_text))
        deadline = parse_date(extract_value(r"Date\s*Limite\s*Candidature\s*:\s*\w+\s*" + date_pattern, full_text))
        #print("Contract Duration:", contract_duration)
        #print("Hiring Date:", hiring_date)
        return [contract_duration, hiring_date, deadline]

    
    def log_missing_fields(self):
        for field in ["title", "location", "description", "contract_type", "salary_mean", "education", "experience", "industry", "skills", "posted_date", "contract_duration", "hiring_date", "deadline"]:
            if not getattr(self, field):
                logging.info(f"Missing {field}")

class CSVHandler:
    """Handles loading and saving job offers to a CSV file."""
    @staticmethod
    def load_existing_ids(filename):
        existing_ids = set()
        if os.path.exists(filename):
            with open(filename, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    existing_ids.add(row[0])
        return existing_ids

    @staticmethod
    def save_to_csv(job_offer, filename):
        if not job_offer:
            return
        
        offer_id = job_offer.url.split("/")[-2]
        existing_ids = CSVHandler.load_existing_ids(filename)
        
        if offer_id in existing_ids:
            logging.info(f"Offer ID {offer_id} already exists. Skipping save.")
            return

        job_data = [
            offer_id, job_offer.title, job_offer.location, job_offer.description, job_offer.contract_type,
            job_offer.salary_mean, job_offer.education, job_offer.experience, job_offer.industry, job_offer.skills,
            job_offer.posted_date, job_offer.hiring_date, job_offer.deadline, job_offer.contract_duration, job_offer.url
        ]
        print("Debbuging:", job_offer.salary_mean)
        file_exists = os.path.exists(filename)
        try:
            with open(filename, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["Offer ID", "Title", "Location", "Description", "Contract Type", "Salary", "Education", "Experience", "Industry", "Skills", "Posted Date", "Hiring Date", "Deadline", "Contract Duration", "URL"])
                writer.writerow(job_data)
            logging.info(f"Job offer {offer_id} saved to {filename}")
        except IOError as e:
            logging.error(f"Error saving to file {filename}: {e}")

class JobScraper:
    """Manages the job scraping process."""
    @staticmethod
    def process_url(url, filename):
        job_offer = JobOffer(url)
        job_offer.extract_offer()
        CSVHandler.save_to_csv(job_offer, filename)

    @staticmethod
    def joboffers(urls, filename):
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(JobScraper.process_url, url, filename) for url in urls]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"Error processing URL: {e}")

if __name__ == "__main__":
    with open("cnrs_jobs.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    urls = [value.get("url") for value in data.values() if value.get("url")]
    print(len(urls))
    JobScraper.joboffers(urls, "data.csv")