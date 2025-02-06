import json
import logging
from datetime import datetime, timedelta
from dict_accessor import DictAccessor



class JobFilter:
    # initialize DictAccessor
    # import get method from DictAccessor

    def __init__(self, job_data, keywords=None):
        self.job_data = job_data
        self.keywords = keywords

    def filter_by_keyword(self, keyword, required=True):
        """Filter job offers by keyword."""
        if required:
            print("Here ONe")
            mylist = [job for job in self.job_data if keyword.lower() in DictAccessor(self.job_data).get(job,"description").lower()]
            print(mylist)
        else:
            print("Here Two")
            mylist = [job for job in self.job_data if keyword.lower() not in DictAccessor(self.job_data).get(job,"description").lower()]
            print(mylist)
            
        for job in mylist:
            #job)d
            #print(DictAccessor(self.job_data).get(job,"deadline",\
            #    DictAccessor(self.job_data).get(job,"title"),\
            #    DictAccessor(self.job_data).get(job,"url")))
            
                                                    
        return mylist
            
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

    @staticmethod
    def load_offers(filename="job_description.json"):
        """Load job offers from a JSON file."""
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
        
    def deadline_filter(self):
        """Categorize job offers by deadline proximity."""
        today = datetime.today()
        print(type(self.job_data))
        for job in self.job_data:
            print("Here",job)
            deadline_str = DictAccessor(self.job_data).get(job, "deadline") 
            #self.job_data[job]["deadline"]
            #deadline_str = self.job_data[job]["deadline"] 
            print("Here",deadline_str)
            #job.get('deadline')
            if not deadline_str:
                print(f"Missing deadline for job: {self.job_data[job]}")
                continue

            try:
                deadline = datetime.strptime(deadline_str, "%d-%m-%Y")
            except ValueError:
                print(f"Invalid date format in job: {self.job_data[job]}")
                continue

            days_left = (deadline - today).days

            if days_left < -1:
                status = "\033[91mEXPIRED\033[0m"  # Red for expired
            elif days_left < 0:
                status = "\033[91mUrgent (Today)\033[0m"  # Red for eminent
            elif days_left == 0:
                status = "\033[91mEminent (Tomorrow)\033[0m"
            elif days_left <= 5:
                status = "\033[93mUpcoming (less than 5 days)\033[0m"  # Orange
            else:
                status = "Available"

            print(f"Job: {DictAccessor(self.job_data).get(job, 'title')}  | Deadline: {deadline_str} | Status: {status} | URL: {DictAccessor(self.job_data).get(job, 'url')}")
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    job_data = JobFilter.load_offers("job_description.json")
    job_filter = JobFilter(job_data)

    #print("\nJob deadlines categorized:")
    #job_filter.deadline_filter()

    from data.keywords import *
    print("\nJob offers filtered by keyword:")
    for keyword in fr_keys:
        print(f"\nKeyword: {keyword}")
        job_filter.filter_by_keyword(keyword, required=True)
        