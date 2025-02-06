class DictAccessor:
    def __init__(self, job_data):
        """Initialize with the dictionary containing job data."""
        self.job_data = job_data

    def get(self, job_name, key, default=None):
        """Retrieve a value given a job name and key."""
        return self.job_data.get(job_name, {}).get(key, default)

if __name__ == "__main__":

    job_data = {
        "blabla": {"deadline": "2025-02-10", "status": "pending"},
        "foo": {"deadline": "2025-03-01", "status": "completed"}
    }

    # Create an instance
    job = DictAccessor(job_data)

    # Access values
    print(job.get("blabla", "deadline"))  # Output: "2025-02-10"
    print(job.get("foo", "status"))       # Output: "completed"
    print(job.get("blabla", "priority", "low"))  # Output: "low" (default value)
