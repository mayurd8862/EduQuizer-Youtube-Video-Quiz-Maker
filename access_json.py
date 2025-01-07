import json
import os


import json

# Function to save JSON data
def save_json(data, filename):
    """
    Save a Python object as a JSON file.
    :param data: The Python object to save (e.g., dict or list).
    :param filename: The name of the JSON file to save.
    """
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving JSON: {e}")

# Function to load JSON data
def load_json(filename):
    """
    Load JSON data from a file.
    :param filename: The name of the JSON file to load.
    :return: The Python object representing the JSON data.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        print(f"Data successfully loaded from {filename}")
        return data
    except Exception as e:
        print(f"An error occurred while loading JSON: {e}")
        return None

