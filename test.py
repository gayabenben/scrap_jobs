from bs4 import BeautifulSoup
import requests

# CNRS URL
url = 'https://emploi.cnrs.fr/Recherche.aspx?bassin=INDEF&type=ITCDD&texte='

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

#print(soup.prettify())
#
class_search = "CphMain_DivSearchResults"
jobs = soup.find_all('div', class_=class_search)
print(jobs)

#for job in jobs:
    #title = job.find('h2').text
    #print(title)
