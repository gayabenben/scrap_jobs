import re
import numpy as np
import logging

class DigitExtractor:
    @staticmethod
    def normalize_number(match: str) -> int:
        """
        Normalize the extracted number into a four-digit integer.
        """
        match = match.replace(" ", "").replace(",", "").replace(".", "")
        return int(match[:4])  # Ensure we return only the first four digits

    @staticmethod
    def extract_numbers(text: str) -> int:
        """
        Extract numbers matching the given patterns and return a the mean value.
        """
        patterns = [
            r'\b\d{4}\b',               # 4 digits
            r'\b\d{4}[,.]\d{2}\b',      # 4.2 digits (e.g., 1234.56 or 1234,56)
            r'\b\d{1,3}(?:[ ,.])\d{3}\b', # 1 3 digits (e.g., 2 555, 12 345)
            r'\b\d{1,3}(?:[ ,.])\d{3}[,.]\d{2}\b', # 1 3.2 (e.g., 2 555.45, 12 345,67)
            r'\b\d{1,3}[.,]\d{3}[,.]\d{2}\b' # 1.3,2 or 1,3.2 (e.g., 2.555,45 or 2,555.45)
        ]
        
        numbers = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            numbers.extend(DigitExtractor.normalize_number(m) for m in matches)
        
        # remove years
        numbers = [n for n in numbers if n < 1900 or n > 2050] 
        print("Found numbers:", numbers)
        if not numbers:
            logging.warning("No numbers found in the text.")
            return 0
        else:
            mean = int(np.mean(numbers))
            return mean