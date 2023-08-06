import csv
from typing import Optional, Dict
import importlib.resources

class NameMatcher:
    """Class to find the gender of a given name by searching in a CSV file.
    """
    instance = None
    name_data: Dict[str, str] = {}

    def __init__(self, file_name: str = "first_names.csv"):
        if not NameMatcher.instance:
            NameMatcher.instance = self
            self.file_name = file_name
            NameMatcher.name_data = self._load_name_data()

    def _load_name_data(self) -> Dict[str, str]:
        """
        Load name data from the CSV file into a dictionary.

        Returns:
            Dict[str, str]: A dictionary with names as keys and gender classification as values.
        """
        name_data = {}

        with importlib.resources.open_text("pt_name_gen", self.file_name) as csvfile:
            csv_reader = csv.DictReader(csvfile)

            for row in csv_reader:
                name = row["name"]
                classification = row["classification"]
                name_data[name] = classification

        return name_data

    def find_name(self, name: str) -> Optional[str]:
        """
        Find the gender of the given name in the CSV file.

        Args:
            name (str): The name to search for.

        Returns:
            Optional[str]: The gender of the name if found, otherwise None.
        """
        name = name.upper()
        return NameMatcher.name_data.get(name, None)

    @staticmethod
    def get_gender(name: str) -> Optional[str]:
        """
        Get the gender of the given name.

        Args:
            name (str): The name to search for.

        Returns:
            Optional[str]: The gender of the name if found, otherwise None.
        """
        if not NameMatcher.instance:
            NameMatcher()
        return NameMatcher.instance.find_name(name)
