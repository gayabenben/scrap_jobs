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

class JobOffer:
    try:
        session = requests.Session()  # Reuse session for better performance
    except Exception as e:
        logging.error(f"Error: {e}")
    
    def __init__(self, title=None, location=None, description=None, contract_type=None, salary=None, education=None, experience=None, industry=None, skills=None, posted_date=None, deadline=None, contract_duration=None, hiring_date=None, url=None):
        self.title = title
        self.location = location
        self.description = description
        self.contract_type = contract_type
        self.salary = salary
        self.education = education
        self.experience = experience
        self.industry = industry
        self.skills = skills
        self.posted_date = posted_date
        self.url = url
        self.contract_duration = contract_duration
        self.hiring_date = hiring_date
        self.deadline = deadline
        self.salary_mean = None


        
    def fetch_html(self):
        """ Fetch and parse the webpage content with enhanced error handling. """
        try:
            response = self.session.get(self.url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred while fetching {self.url}: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Connection error occurred while fetching {self.url}: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"Timeout error occurred while fetching {self.url}: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"General error occurred while fetching {self.url}: {req_err}")
        return None

    @staticmethod
    def extract_text(soup, selector):
        """ Extract text using CSS selectors for better flexibility. """
        element = soup.select_one(f'span[itemprop="{selector}"]')
        return element.text.strip() if element else None
    
    
    
    @staticmethod
    def clean_title(title):
        """ Clean job titles by removing unwanted suffixes. """
        if title:
            return title.replace(' (H/F)', '').replace(' H/F', '')
        return None
    
        
    def extract_dates(self):
        soup = self.fetch_html()
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
            if date_str is None:
                print("Warning: date_str is None")  # Debugging
                return None

            try:
                locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
                return datetime.strptime(date_str, "%d %m %Y").strftime("%d-%m-%Y")
            except ValueError:
                return None
        """
        def parse_date(date_str):
            '''Convert French date format to 'DD-MM-YYYY'.'''
            try:
                locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
                return datetime.strptime(date_str, "%d %m %Y").strftime("%d-%m-%Y")
            except ValueError:
                return None
        """
        contract_duration = extract_value(r"Durée\s*du\s*contrat\s*:\s*(\d+\s*mois)", full_text)
        hiring_date = parse_date(extract_value(r"Date\s*d['’]embauche\s*prévue\s*:\s*" + date_pattern, full_text))
        deadline = parse_date(extract_value(r"Date\s*Limite\s*Candidature\s*:\s*\w+\s*" + date_pattern, full_text))
        
        return [contract_duration, hiring_date, deadline]
        
    def extract_new_offer(self):
        """ Extract only the new job offers. """
        soup = self.fetch_html()
        if not soup:
            return None
        json_offer = "job_offers.json"
        # load the json file
        # check if file exists
        if os.path.exists("job_offers.json"):
            with open("job_offers.json", "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = {}
                    logging.error(f"Error loading JSON file {json_offer}.")
        else:
            existing_data = {}
        
        # extract the offer id
        offer_id = self.url.split("/")[-2]
        # check if the offer id is already in the json file
        if offer_id in existing_data:
            logging.info(f"Offer ID {offer_id} already exists. Skipping save.")
            return None
        else:
            logging.info(f"New offer ID {offer_id} found. Saving to JSON file.")
            return self.extract_offer()
        
        
    def extract_offer(self):
        """ Extract job details and populate instance attributes. """
        soup = self.fetch_html()
        if not soup:
            return None  # Return None if fetching failed
        try:
            self.title = self.clean_title(self.extract_text(soup, 'title'))
            self.location = self.extract_text(soup, 'addressLocality')
            self.description = self.extract_text(soup, 'description')
            self.contract_type = self.extract_text(soup, 'employmentType')
            self.salary = self.extract_text(soup, 'baseSalary')
            self.salary_mean = self.get_salary()
            if int(self.salary_mean) < 1200:
                logging.info(f"Low salary detected: {self.salary} from {self.url}, an error may have occurred when extracting salary mean {self.salary_mean}")
            self.education = self.extract_text(soup, 'educationRequirements')
            self.experience = self.extract_text(soup, 'experienceRequirements')
            self.industry = self.extract_text(soup, 'industry')
            self.skills = self.extract_text(soup, 'skills')
            self.posted_date = self.extract_text(soup, 'datePosted')
            self.contract_duration, self.hiring_date, self.deadline = self.extract_dates()
            print("NOWWWWWWWWWWWWWWWWWWWWWWWWWWWWw", self.title)
        except Exception as e:
            logging.error(f"Error extracting job offer details: {e}")
        return self  # Return instance with populated data
    
    def get_salary(self):
        #print("SALARY", self.salary)
        s = self.salary
        try:
            numbers = [float(x.replace('.', '')) for x in re.findall(r'\d+?\d*', s)]
            numbers = [float(x.replace(',')) for x in re.findall(r'\d+[,.]?\d*', s)]
            return int(np.mean(numbers))
        except Exception as e:
            logging.error(f"Error processing salary: {e}")
            return None
    
    def save_to_json(self, filename="job_description.json"):
        """Save job offer data to a JSON file, ensuring no duplicates."""
        offer_id = self.url.split("/")[-2]
        job_data = {
            offer_id: {
                "title": self.title,
                "location": self.location,
                "description": self.description,
                "contract_type": self.contract_type,
                "salary": self.salary_mean,
                "education": self.education,
                "experience": self.experience,
                "industry": self.industry,
                "skills": self.skills,
                "date_posted": self.posted_date,
                "starting": self.hiring_date,
                "deadline": self.deadline,
                "contract_duration": self.contract_duration,
                "url": self.url
            }
        }

        try:
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = {}
            else:
                existing_data = {}

            if offer_id in existing_data:
                logging.info(f"Offer ID {offer_id} already exists. Skipping save.")
                return

            existing_data.update(job_data)

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, indent=4, ensure_ascii=False)
            logging.info(f"Job offer data saved to {filename}")
        except IOError as e:
            logging.error(f"Error saving file {filename}: {e}")
            return None
        
    def joboffer(url):
        """Runs the JobOffer class."""
        #url = "https://emploi.cnrs.fr/Offres/CDD/UMR7325-VALSEV-138/Default.aspx"
        job_offer = JobOffer(url=url)
        job_offer.extract_new_offer()
        job_offer.extract_offer()
        job_offer.extract_dates()
        job_offer.save_to_json()
        return job_offer
    
    def url_saved(self, diction):
        soup = self.fetch_html()
        if not soup:
            return None
        #json_offer = "job_offers.json"
        
        #job_offer = JobOffer(url=url)
        
        # load dict
        print(diction.values())
        return None
        
        
    def joboffers(urls):
        """Runs the JobOffer class for multiple URLs."""
        for url in urls:
            
            JobOffer.joboffer(url)
        logging.info("All job offers processed.")
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    
    dictionnary = json.load(open("job_offers.json", "r", encoding="utf-8"))   
    
    #print(dictionnary)
    #urls = [key['url'] for value, key in enumerate(dictionnary)]
    #JobOffer.url_saved(dictionnary)
    #print(urls)
    #JobOffer.joboffers(urls)
    # select only 2 keys from dict
    
    i = 0
    my_urls = []
    
    for key, value in enumerate(dictionnary):#list(dictionnary.items())[:2]):
        print(key, value)
        #print(dictionnary[value]["url"])
        #while i<10:
            #JobOffer.joboffer(dictionnary[value]['url'])
            #i += 1
        my_urls.append(dictionnary[value]["url"])
    
    JobOffer.joboffers(my_urls)
    
    
    #job_offer.extract_offer()
    
    
    
    #job_offer.extract_dates()
    #job_offer.save_to_json()
