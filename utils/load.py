import json
import logging
import os

class Load:
    
    def __init__(self, filename: str) -> None:
        """Initialize with the filename."""
        self.filename = filename
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        
    def save_to_json(self, data: dict) -> None:
        """
        Save data to a JSON file.
        If the file already exists, it will overwrite the existing content.
        """
        if not isinstance(data, dict):
            logging.error("Data must be a dictionary.")
            return
        
        try:
            with open(self.filename, "w", encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            logging.info(f"Data successfully saved to {self.filename}.")
        except Exception as e:
            logging.error(f"Error saving data to {self.filename}: {e}")
    
    def load_from_json(self) -> dict:
        """
        Load data from a JSON file.
        Returns an empty dictionary if the file doesn't exist or if there's an error.
        """
        if not os.path.exists(self.filename):
            logging.error(f"File {self.filename} not found.")
            return {}

        try:
            with open(self.filename, "r", encoding='utf-8') as file:
                data = json.load(file)
            logging.info(f"Data successfully loaded from {self.filename}.")
            return data
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {self.filename}: {e}")
            return {}
        except Exception as e:
            logging.error(f"Error loading data from {self.filename}: {e}")
            return {}

if __name__ == "__main__":
    loader = Load("data.json")
    data = {"name": "Alice", "age": 30, "city": "New York"}
    loader.save_to_json(data)
    loaded_data = loader.load_from_json()