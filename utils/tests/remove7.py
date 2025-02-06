from datetime import datetime
import locale
from bs4 import BeautifulSoup

class JobOffer:
    def fetch_html(self):
        """Simulating the HTML fetching step"""
        # Replace with actual method that fetches HTML content
        return """
        <div id="CphMain_OffreAffichage1" class="OffreAffichage">
        <div class="OffreDetailMain" itemscope itemtype="http://schema.org/JobPosting">
            <div class="OffreDetailMainInfosGenerales">
                <h3>Informations générales</h3>
                <p><strong>Intitulé de l'offre : <span itemprop="title">Ingénieur-e biologiste en analyse de données H/F</span></strong>
                <br />Référence : UMR9213-MATGUI0-013<br />
                Nombre de Postes : 1<br />
                Lieu de travail : <span itemprop="jobLocation" itemscope itemtype="http://schema.org/Place">
                <span itemprop="address" itemscope itemtype="http://schema.org/PostalAddress">
                <span itemprop="addressLocality">ORSAY</span></span></span><br />
                Date de publication : <span itemprop="datePosted">mercredi 29 janvier 2025</span><br />
                Type de contrat : <span itemprop="employmentType">IT en contrat CDD</span><br />
                Durée du contrat : 9 mois<br />
                Date d'embauche prévue : 1 avril 2025<br />
                Date limite de candidature : 15 février 2025<br />
                Quotité de travail : <span itemprop="workHours">Complet</span><br />
                Rémunération : <span itemprop="baseSalary">Entre 2932,84€ à 3302,85€ selon expérience</span><br />
                Niveau d'études souhaité : <span itemprop="educationRequirements">BAC+5</span><br />
                Expérience souhaitée : <span itemprop="experienceRequirements">Indifférent</span><br />
                BAP : A - Sciences du vivant, de la terre et de l'environnement<br />
                Emploi type : <span itemprop="industry">Ingénieur-e biologiste en analyse de données</span><br />
            </p></div></div></div>
        """
    
    def extract_dates(self):
        """Extract contract duration, hiring date, and application deadline from the HTML content."""
        soup = BeautifulSoup(self.fetch_html(), "html.parser")
        
        # Use CSS selectors to directly extract required text
        contract_duration = None
        hiring_date = None
        deadline = None

        # Extract contract duration
        duration_tag = soup.find("p", string=lambda text: text and "Durée du contrat" in text)
        if duration_tag:
            contract_duration = duration_tag.get_text(strip=True).split(":")[-1].strip()

        # Extract hiring date (Date d'embauche prévue)
        hiring_date_tag = soup.find("p", string=lambda text: text and "Date d'embauche prévue" in text)
        if hiring_date_tag:
            hiring_date_str = hiring_date_tag.get_text(strip=True).split(":")[-1].strip()
            try:
                locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')  # Ensure French locale
                hiring_date = datetime.strptime(hiring_date_str, "%d %B %Y")
            except ValueError as e:
                print(f"Error converting hiring date: {e}")
                hiring_date = None
        
        deadline_match = re.search(r"Date\s*Limite\s*Candidature\s*:\s*\w+\s*(\d{1,2} [a-zA-Zéû]+ \d{4})", full_text, re.IGNORECASE)
        print(deadline_match[0])
        if deadline_match:
            deadline_str = deadline_match.group(1)
            try:
                deadline = datetime.strptime(deadline_str, "%d %B %Y").strftime("%d-%m-%Y")
            except ValueError as e:
                print(f"Error parsing deadline: {e}")
                deadline = None
        
        """
        # Extract application deadline (Date limite de candidature)
        deadline_tag = soup.find("p", string=lambda text: text and "Date limite de candidature" in text)
        if deadline_tag:
            deadline_str = deadline_tag.get_text(strip=True).split(":")[-1].strip()
            try:
                deadline = datetime.strptime(deadline_str, "%d %B %Y")
            except ValueError as e:
                print(f"Error converting deadline date: {e}")
                deadline = None
"""
        # Return the results in the required format (DD-MM-YYYY)
        return {
            'contract_duration': contract_duration,
            'hiring_date': hiring_date.strftime("%d-%m-%Y") if hiring_date else None,
            'deadline': deadline.strftime("%d-%m-%Y") if deadline else None
        }

# Example usage
job_offer = JobOffer()
job_dates = job_offer.extract_dates()
print(job_dates)
