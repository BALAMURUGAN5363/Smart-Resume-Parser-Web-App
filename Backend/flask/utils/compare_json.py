"""import json

# Load two JSON files
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Compare two JSON structures
def compare_json(json1, json2):
    score1 = evaluate_json(json1)
    score2 = evaluate_json(json2)

    print(f"JSON 1 Score: {score1}")
    print(f"JSON 2 Score: {score2}")

    if score1 > score2:
        print("JSON 1 is better!")
        return json1
    elif score2 > score1:
        print("JSON 2 is better!")
        return json2
    else:
        print("Both JSON files are equally good!")
        return None

# Evaluation function: Higher score = better JSON
def evaluate_json(json_data):
    score = 0
    if isinstance(json_data, dict):
        score += len(json_data)  # More keys = better structure
        score -= sum(1 for v in json_data.values() if v in [None, "", []])  # Penalize missing values

    elif isinstance(json_data, list):
        score += len(json_data)  # Larger lists = more data
        for item in json_data:
            if isinstance(item, dict):
                score += len(item)  # Nested completeness

    return score

# Load JSON files
json_file1 = "H:/OCR/Ocr/Scripts/output.json"
json_file2 = "H:/OCR/Ocr/Scripts/categorized_invoice_data.json"

json1 = load_json(json_file1)
json2 = load_json(json_file2)

# Compare and get the better JSON
better_json = compare_json(json1, json2)

# Save the better JSON
if better_json:
    with open("better_output.json", "w", encoding="utf-8") as output_file:
        json.dump(better_json, output_file, indent=4, ensure_ascii=False)
    print("Better JSON saved as 'better_output.json'")"""
"""import json

# Load two JSON files
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Compare two JSON structures
def compare_json(json1, json2):
    score1 = evaluate_json(json1)
    score2 = evaluate_json(json2)

    print(f"JSON 1 Score: {score1}")
    print(f"JSON 2 Score: {score2}")

    if score1 > score2:
        print("JSON 1 is better!")
        return json1
    elif score2 > score1:
        print("JSON 2 is better!")
        return json2
    else:
        print("Both JSON files are equally good!")
        return None

# Evaluation function: Higher score = better JSON
def evaluate_json(json_data):
    score = 0
    if isinstance(json_data, dict):
        score += len(json_data)  # More keys = better structure
        score -= sum(1 for v in json_data.values() if v in [None, "", []])  # Penalize missing values

    elif isinstance(json_data, list):
        score += len(json_data)  # Larger lists = more data
        for item in json_data:
            if isinstance(item, dict):
                score += len(item)  # Nested completeness

    return score

# Load JSON files
json_file1 = "H:/OCR/Ocr/Scripts/output.json"
json_file2 = "H:/OCR/Ocr/Scripts/categorized_invoice_data.json"

json1 = load_json(json_file1)
json2 = load_json(json_file2)

# Compare and get the better JSON
better_json = compare_json(json1, json2)

# Save the better JSON
if better_json:
    with open("better_output.json", "w", encoding="utf-8") as output_file:
        json.dump(better_json, output_file, indent=4, ensure_ascii=False)
    print("Better JSON saved as 'better_output.json'")
def evaluate_json(json_data):
    score = 0
    if isinstance(json_data, dict):
        score += len(json_data)
        score -= sum(1 for v in json_data.values() if v in [None, "", [], {}])
        for v in json_data.values():
            if isinstance(v, dict):
                score += len(v)
                score -= sum(1 for vv in v.values() if vv in [None, "", [], {}])
            elif isinstance(v, list):
                score += len(v)
                for item in v:
                    if isinstance(item, dict):
                        score += len(item)
                        score -= sum(1 for iv in item.values() if iv in [None, "", [], {}])
    elif isinstance(json_data, list):
        score += len(json_data)
        for item in json_data:
            if isinstance(item, dict):
                score += len(item)
                score -= sum(1 for v in item.values() if v in [None, "", [], {}])
    return score

def compare_jsons(json_list):
    best_json = None
    best_score = -1
    for j in json_list:
        if not j or not isinstance(j, (dict, list)):
            continue
        score = evaluate_json(j)
        if score > best_score:
            best_score = score
            best_json = j
    return best_json"""
import json

def evaluate_json(json_data):
    score = 0
    if isinstance(json_data, dict):
        score += len(json_data)
        #addition score
        score -= sum(1 for v in json_data.values() if v in [None, "", [], {}])
        #subraction the code while the {},"", these are empty
        for v in json_data.values():
            if isinstance(v, dict):
                score += len(v)
                score -= sum(1 for vv in v.values() if vv in [None, "", [], {}])
            elif isinstance(v, list):
                score += len(v)
                for item in v:
                    if isinstance(item, dict):
                        score += len(item)
                        score -= sum(1 for iv in item.values() if iv in [None, "", [], {}])
        #If a value is a nested dictionary, score its completeness too
    elif isinstance(json_data, list):
        score += len(json_data)
        for item in json_data:
            if isinstance(item, dict):
                score += len(item)
                score -= sum(1 for v in item.values() if v in [None, "", [], {}])
    return score
def compare_jsons(json_list):
    best_json = None
    best_score = -1
    for j in json_list:
        score = evaluate_json(j)
        if score > best_score:
            best_score = score
            best_json = j
    return best_json





