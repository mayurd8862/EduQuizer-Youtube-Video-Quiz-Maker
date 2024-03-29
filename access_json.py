import json
import os

json_file_path = os.path.join(os.getcwd(),'Youtube video Quize','result.json')

# Load the JSON data from the file
with open(json_file_path, "r") as file:
    data = json.load(file)

# Now you can access the data as a list of dictionaries
for entry in data:
    name = entry["name"]
    questions = entry["questions"]
    score = entry["score"]
    
    print(f"Name: {name}")
    print(f"Score: {score}")
    print("Questions:")
    for question in questions:
        print(question[0])
        print(f"Correct Answer: {question[1]}")
        print(f"Options: {', '.join(question[1:])}")
        print()
