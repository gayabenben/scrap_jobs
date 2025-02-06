from bs4 import BeautifulSoup

def extract_job_details(soup):
    """Extract important job details like publication date, contract duration, and hiring date."""
    
    # Extraire la date de publication
    date_posted = soup.select_one('span[itemprop="datePosted"]')
    date_posted = date_posted.text.strip() if date_posted else None
    
    # Extraire la durée du contrat
    contract_duration = soup.select_one('p:contains("Durée du contrat")')
    # find the line containing the contract duration
    contract_duration = soup.find('p', text='Durée du contrat')
    #contract_duration = contract_duration.text.strip() if contract_duration else None
    #contract_duration = 
    # Extraire la date d'embauche prévue
    hiring_date = soup.select_one('span[itemprop="datePosted"]')
    hiring_date = hiring_date.text.strip() if hiring_date else None
    
    # Retourner les données sous forme de dictionnaire
    return {
        'date_posted': date_posted,
        'contract_duration': contract_duration,
        'hiring_date': hiring_date
    }

# Exemple d'utilisation
html_content = """<div id="CphMain_OffreAffichage1" class="OffreAffichage"><div class="OffreDetailMain" itemscope itemtype="http://schema.org/JobPosting">
<div class="OffreDetailMainInfosGenerales">
<h3>Informations générales</h3><p><strong>Intitulé de l'offre : <span itemprop="title">Ingénieur-e biologiste en analyse de données H/F</span></strong>
<br />Référence : UMR9213-MATGUI0-013<br />
Nombre de Postes : 1<br />
Lieu de travail : <span itemprop="jobLocation" itemscope itemtype="http://schema.org/Place"><span itemprop="address" itemscope itemtype="http://schema.org/PostalAddress"><span itemprop="addressLocality">ORSAY</span></span></span><br />
Date de publication : <span itemprop="datePosted">mercredi 29 janvier 2025</span><br />
Type de contrat : <span itemprop="employmentType">IT en contrat CDD</span><br />
Durée du contrat : 9 mois<br />
Date d'embauche prévue : 1 avril 2025<br />Quotité de travail : <span itemprop="workHours">Complet</span><br />
Rémunération : <span itemprop="baseSalary">Entre 2932,84€ à 3302,85€ selon expérience</span><br />
Niveau d'études souhaité : <span itemprop="educationRequirements">BAC+5</span><br />
Expérience souhaitée : <span itemprop="experienceRequirements">Indifférent</span><br />
BAP : A - Sciences du vivant, de la terre et de l'environnement<br />
Emploi type : <span itemprop="industry">Ingénieur-e biologiste en analyse de données</span><br />
</p></div></div></div>"""

soup = BeautifulSoup(html_content, 'html.parser')
job_details = extract_job_details(soup)
print(job_details)
