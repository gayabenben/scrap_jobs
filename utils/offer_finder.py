import requests
import json
from bs4 import BeautifulSoup

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def extract_text(soup, itemprop):
    element = soup.find('span', itemprop=itemprop)
    return element.text.strip() if element else None

def clean_title(title):
    if title:
        return title.replace(' (H/F)', '').replace(' H/F', '')
    return None

def extract_job_details(offer_url):
    soup = fetch_html(offer_url)
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
    job_offers = {i+1: extract_job_details(url) for i, url in enumerate(url_list)}
    save_to_json(job_offers)
