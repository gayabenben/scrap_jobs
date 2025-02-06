import json
import logging


class JobFilter:
    def __init__(self, job_data=None):
        """Initialize with job data (list of job offers)."""
        self.job_data = job_data if job_data else []

    @classmethod
    def from_json(cls, filename="job_description.json"):
        """Load job offers from a JSON file and return a JobFilter instance."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                job_offers = json.load(f)
                job_list = list(job_offers.values())  # Extract job offers
            return cls(job_list)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading JSON: {e}")
            return cls()

    def filter_by_keywords(self, keywords, include=True):
        """Filter jobs where at least one keyword appears in the description."""
        if include:
            return [
                job for job in self.job_data
                if any(keyword.lower() in job.get('description', '').lower() for keyword in keywords)
            ]
        else:
            return [
                job for job in self.job_data
                if all(keyword.lower() not in job.get('description', '').lower() for keyword in keywords)
            ]

    def filter_by_title(self, title):
        """Filter jobs by title."""
        return [job for job in self.job_data if title.lower() in job.get('title', '').lower()]

    def filter_by_location(self, location):
        """Filter jobs by location."""
        return [job for job in self.job_data if location.lower() in job.get('location', '').lower()]

    def filter_by_salary(self, min_salary, max_salary):
        """Filter jobs within a salary range."""
        return [
            job for job in self.job_data
            if job.get('salary') and min_salary <= float(job['salary']) <= max_salary
        ]

    def filter_by_duration(self, min_months):
        """Filter jobs by contract duration in months."""
        return [
            job for job in self.job_data
            if job.get('contract_duration') and int(job['contract_duration'].split()[0]) >= min_months
        ]
    
    def filter_by_diploma(self, education):
        """Filter jobs by required education level."""
        return [job for job in self.job_data if "BAC+5" in job.get('education', '').lower() or "BAC+8" in job.get('education', '').lower() or "BAC +3" in job.get('education', '').lower() or "BAC +8" in job.get('education', '').lower()]

    def save_to_json(self, filename):
        """Save filtered jobs to a JSON file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.job_data, f, indent=4, ensure_ascii=False)


# Example Usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Load job offers
    job_filter = JobFilter.from_json("job_description.json")

    # Define English & French keyword lists
    eng_keys = [
        'data science', 'machine learning', 'data analysis', 'big data', 'python', 'r', 'sql',
        'analytics', 'statistics', 'ai', 'deep learning', 'pandas', 'numpy'
    ]
    
    fr_keys = [
        'science des données', 'apprentissage automatique', 'analyse de données', 'big data', 'python', 'r', 'sql',
        'statistiques', 'intelligence artificielle', 'apprentissage profond', 'réseaux neuronaux', 'informatique'
    ]

    forbidden_keys = ['senior', 'manager', 'director', 'lead', 'head', 'chief', 'vp', 'president']
    # Apply filters
    #filtered_jobs = job_filter.filter_by_keywords(fr_keys, include=True)
    #filtered_jobs = filtered_jobs.filter_by_keywords(eng_keys, include=True)
    #filtered_jobs = job_filter.filter_by_keywords(forbidden_keys, include=False)
    
    filtered_jobs = job_filter.filter_by_salary(3000, 50000)
    # Print results
    print(f"Found {len(filtered_jobs)} job(s) matching keywords.")
    #for job in filtered_jobs:
    #    print(f"Title: {job.get('title', 'N/A')} | Location: {job.get('location', 'N/A')}")

    # Save results
    job_filter.save_to_json("filtered_jobs.json")
