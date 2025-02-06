import json
import logging


class JobFilter:

    def __init__(self, job_data, keywords=None):
        self.job_data = job_data
        self.keywords = keywords

    #def filter_by_keyword(self, keyword):
    #    """Filter job offers by keyword."""
    #    return [job for job in self.job_data if keyword.lower() in job['description'].lower()]
    def ifilter_by_keyword(self, keyword):
        # if at least one keyword is in the description
        
        #if any(keyword.lower() in job['description'].lower() for job in self.job_data):
        #    return True
        return [job for job in self.job_data if keyword.lower() in job['description'].lower() if any(keyword.lower() in job['description'].lower() for job in self.job_data)]
    
    #def keep_job(self, job):
    #    ifilter_by_keyword(job)
    
        

    def filter_keywords(self, keywords):
        """Filter job offers by multiple keywords."""
        return [job for job in self.job_data if any(keyword.lower() in job['description'].lower() for keyword in keywords)]

    def filter_by_title(self, title):
        """Filter job offers by title."""
        return [job for job in self.job_data if title.lower() in job['title'].lower()]

    def filter_by_location(self, location):
        """Filter job offers by location."""
        return [job for job in self.job_data if location.lower() in job['location'].lower()]

    def filter_by_salary(self, min_salary, max_salary):
        """Filter job offers by salary range."""
        return [job for job in self.job_data if job['salary'] and min_salary <= float(job['salary']) <= max_salary]

    def filter_by_skills(self, skills):
        """Filter job offers by required skills."""
        return [job for job in self.job_data if skills.lower() in job['skills'].lower()]

    def save_to_json(self, filename):
        """Save filtered job data to a JSON file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.job_data, f, indent=4)
            
    def load_offers(self, filename="job_description.json"):
        """Load job offers from a JSON file."""
        with open(filename, "r", encoding="utf-8") as f:
            job = json.load(f)
            self.job_data = job["UMR8023-OLGHOD-004"]["description"]
    #print(job_data)
       
            
            
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO) 
    
    JobFilter.load_offers("job_description.json")
    eng_keys = ['data science', 'machine learning', 'data analysis', 'big data', 'python', 'r', 'sql', 'data', 'analytics', 'statistics', 'ai', 'artificial intelligence', 'deep learning', 'neural networks', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'keras', 'pytorch', 'tableau', 'power bi', 'data visualization', 'data mining', 'predictive modeling', 'regression', 'classification', 'clustering', 'nlp', 'natural language processing', 'computer vision', 'reinforcement learning', 'time series', 'forecasting', 'anomaly detection', 'unsupervised learning', 'supervised learning', 'ensemble learning', 'feature engineering', 'feature selection', 'model evaluation', 'model selection', 'model deployment', 'data cleaning', 'data preprocessing', 'data wrangling', 'data transformation', 'data integration', 'data governance', 'data quality', 'data validation']
     
    fr_keys = ['données', 'science des données', 'apprentissage automatique', 'analyse de données', 'big data', 'python', 'r', 'sql', 'analyse de données', 'statistiques', 'ia', 'intelligence artificielle', 'apprentissage profond', 'réseaux neuronaux', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'keras', 'pytorch', 'tableau', 'power bi', 'visualisation de données', 'exploration de données', 'modélisation prédictive', 'régression', 'classification', 'regroupement', 'nlp', 'traitement du langage naturel', 'vision par ordinateur', 'apprentissage par renforcement', 'séries temporelles', 'prévision', 'détection d\'anomalies', 'apprentissage non supervisé', 'apprentissage supervisé', 'apprentissage par ensemble', 'ingénierie des fonctionnalités', 'sélection des fonctionnalités', 'évaluation des modèles', 'sélection des modèles', 'déploiement des modèles', 'nettoyage des données', 'prétraitement des données', 'traitement des données', 'intégration des données', 'gouvernance des données', 'qualité des données', 'validation des données']
    
    ifilter_by_keyword(fr_keys)
    #ifilter_by_keyword(eng_keys)