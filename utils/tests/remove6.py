from datetime import datetime
import locale
import re
from bs4 import BeautifulSoup

class JobOffer:
    def fetch_html(self):
        """Simulating the HTML fetching step"""
        # This should be replaced by the actual method that fetches the HTML content
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
        soup = self.fetch_html()
        print("soup:", soup)  # Debugging: check the raw HTML content

        # Extraire la durée du contrat
        contract_duration_text = soup.find(text=re.compile("Durée du contrat"))
        contract_duration = None
        if contract_duration_text:
            contract_duration = contract_duration_text.split(":")[-1].strip()
        print("contract_duration:", contract_duration)  # Debugging: see the extracted contract duration
        
        # Extraire la date d'embauche prévue
        hiring_date_text = soup.find(text=re.compile("Date d'embauche prévue"))
        print("hiring date text:", hiring_date_text)  # Debugging: check the hiring date text
        if hiring_date_text:
            hiring_date = hiring_date_text.split(":")[-1].strip()
            try:
                locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')  # Ensure French locale is set
                hiring_date = datetime.strptime(hiring_date, "%d %B %Y")
            except ValueError as e:
                print(f"Erreur de conversion de la date d'embauche : {e}")
                hiring_date = None
        
        # Extraire la date limite de candidature
        deadline_text = soup.find(text=re.compile("Date limite de candidature"))
        print("deadline text:", deadline_text)  # Debugging: check the deadline text
        if deadline_text:
            deadline = deadline_text.split(":")[-1].strip()
            try:
                deadline = datetime.strptime(deadline, "%d %B %Y")
            except ValueError as e:
                print(f"Erreur de conversion de la date limite : {e}")
                deadline = None
        
        # Retourner un dictionnaire avec uniquement les dates au format "DD-MM-YYYY"
        return {
            'contract_duration': contract_duration,
            'hiring_date': hiring_date.strftime("%d-%m-%Y") if hiring_date else None,
            'deadline': deadline.strftime("%d-%m-%Y") if deadline else None
        }

# Exemple d'utilisation
job_offer = JobOffer()
job_dates = job_offer.extract_dates()
print(job_dates)
