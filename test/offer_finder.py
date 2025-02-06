import requests
import json
from bs4 import BeautifulSoup
import logging

class JobOffer:
    session = requests.Session()  # Reuse session for better performance
    
    def __init__(self, title, location, description, contract_type, salary, education, experience, industry, skills, url):
        self.title = title
        self.location = location
        self.description = description
        self.contract_type = contract_type
        self.salary = salary
        self.education = education
        self.experience = experience
        self.industry = industry
        self.skills = skills
        self.url = url
            
    def fetch_html(self):
        """ Fetches the HTML content of a webpage """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f"Error: {e}")
            return None
        
    def extract_text(soup, itemprop):
        """ Extracts text from a webpage """
        element = soup.find('span', itemprop=itemprop)
        return element.text.strip() if element else None

    def clean_title(title):
        if title:
            return title.replace(' (H/F)', '').replace(' H/F', '')
        return None

    def extract_offer(offer_url):
        """ 
        Works specifically for the CNRS job offers website.
        """
        soup = fetch_html(self, offer_url)
        job_data = {
            "title": clean_title(extract_text(soup, 'title')),
            "location": extract_text(soup, 'addressLocality'),
            "description": extract_text(soup, 'description'),
            "contract_type": extract_text(soup, 'employmentType'),
            "salary": extract_text(soup, 'baseSalary'),
            "education": extract_text(soup, 'educationRequirements'),
            "experience": extract_text(soup, 'experienceRequirements'),
            "industry": extract_text(soup, 'industry'),
            "skills": extract_text(soup, 'skills'),
            "url": offer_url
        }
        return job_data

    def save_to_json(data, filename="job_desct.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Job offer data saved to {filename}")

if __name__ == "__main__":
    
    url_list = ["https://emploi.cnrs.fr/Offres/CDD/UMR9213-MATGUI0-013/Default.aspx", "https://emploi.cnrs.fr/Offres/CDD/UAR3601-ANILEF-033/Default.aspx"]  # Replace with actual URLs
    job_offers = {i+1: extract_offer (url) for i, url in enumerate(url_list)}
    save_to_json(job_offers)
