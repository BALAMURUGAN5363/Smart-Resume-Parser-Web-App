import spacy

# Load spaCy model once at the top level
nlp = spacy.load("en_core_web_sm")

def run_spacy(extracted_text):
    """
    Process extracted text using spaCy NER, returning structured entity data per page.
    
    :param extracted_text: Full OCR or extracted text, expected to be split by "--- Page N ---"
    :return: A dictionary with named entities grouped by page
    """
    pages = extracted_text.split("--- Page ")
    invoice_data = {}

    for page in pages[1:]:
        parts = page.split("---\n", 1)
        if len(parts) < 2:
            continue
        page_number, page_content = parts
        page_number = page_number.strip()
        page_content = page_content.strip()
        
        doc = nlp(page_content)

        # Extract named entities dynamically
        page_data = {"page": page_number, "text": page_content, "entities": {}}
        for ent in doc.ents:
            if ent.label_ not in page_data["entities"]:
                page_data["entities"][ent.label_] = ent.text
            elif isinstance(page_data["entities"][ent.label_], list):
                page_data["entities"][ent.label_].append(ent.text)
            else:
                page_data["entities"][ent.label_] = [
                    page_data["entities"][ent.label_], ent.text
                ]

        invoice_data[f"page_{page_number}"] = page_data

    return invoice_data

"""
import spacy
import json
import re

# Load pre-trained NLP model
nlp = spacy.load("en_core_web_sm")

# Read OCR output text from file
with open("H:/OCR/output.txt", "r", encoding="utf-8") as file:
    extracted_text = file.read()

# Split text by pages using regex
pages = re.split(r"--- Page (\d+) ---", extracted_text)

# Dictionary to store extracted and categorized data
invoice_data = {"invoice_details": {}, "billing_info": {}, "transaction_details": {}, "banking_info": {}}

for i in range(1, len(pages), 2):  # Pages are split into (Page Number, Content)
    page_number = pages[i].strip()  # Extract the page number
    page_content = pages[i + 1].strip()  # Extract the page text

    # Define regex patterns for different categories
    key_patterns = {
        "invoice_number": (r"Invoice\s*(?:No|Number|ID):\s*(\d+)", "invoice_details"),
        "customer_number": (r"Customer\s*No:\s*(\d+)", "invoice_details"),
        "invoice_date": (r"Date:\s*([\w\s\d.]+)", "invoice_details"),
        "total_amount": (r"Total\s*([\d,.]+)\s*€", "transaction_details"),
        "vat_amount": (r"VAT\s*\d+\s*%\s*([\d,.]+)\s*€", "transaction_details"),
        "gross_amount": (r"Gross\s*Amount.*?([\d,.]+)\s*€", "transaction_details"),
        "iban": (r"IBAN\s*([\w\d\s]+)", "banking_info"),
    }

    # Extract key-value pairs using regex and categorize them
    for key, (pattern, category) in key_patterns.items():
        match = re.search(pattern, page_content, re.IGNORECASE)
        if match:
            invoice_data[category][key] = match.group(1).strip()

    # Use NLP to detect customer name and company name
    doc = nlp(page_content)

    for ent in doc.ents:
        if ent.label_ == "ORG" and "company_name" not in invoice_data["billing_info"]:
            invoice_data["billing_info"]["company_name"] = ent.text
        elif ent.label_ == "PERSON":  # Extracts the correct customer name
            if "customer_name" not in invoice_data["billing_info"] or len(ent.text) > len(
                invoice_data["billing_info"].get("customer_name", "")
            ):
                invoice_data["billing_info"]["customer_name"] = ent.text

# Convert extracted data to JSON
json_output = json.dumps(invoice_data, indent=4)
print(json_output)

# Save output to JSON file
with open("categorized_invoice_data.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_output)
"""
"""

import spacy
import json
import re

# Load pre-trained NLP model
nlp = spacy.load("en_core_web_sm")

# Read OCR output text from file
with open("H:/OCR/output.txt", "r", encoding="utf-8") as file:
    extracted_text = file.read()

# Split text by pages using regex
pages = re.split(r"--- Page (\d+) ---", extracted_text)

# Dictionary to store extracted and categorized data
invoice_data = {"invoice_details": {}, "billing_info": {}, "transaction_details": {}, "banking_info": {}}

for i in range(1, len(pages), 2):  # Pages are split into (Page Number, Content)
    page_number = pages[i].strip()  # Extract the page number
    page_content = pages[i + 1].strip()  # Extract the page text

    # Define regex patterns for different categories
    key_patterns = {
        "invoice_number": (r"Invoice\s*(?:No|Number|ID):\s*(\d+)", "invoice_details"),
        "customer_number": (r"Customer\s*No:\s*(\d+)", "invoice_details"),
        "invoice_date": (r"Date:\s*([\w\s\d.]+)", "invoice_details"),
        "total_amount": (r"Total\s*([\d,.]+)\s*€", "transaction_details"),
        "vat_amount": (r"VAT\s*\d+\s*%\s*([\d,.]+)\s*€", "transaction_details"),
        "gross_amount": (r"Gross\s*Amount.*?([\d,.]+)\s*€", "transaction_details"),
        "iban": (r"IBAN\s*([\w\d\s]+)", "banking_info"),
    }

    # Extract key-value pairs using regex and categorize them
    for key, (pattern, category) in key_patterns.items():
        match = re.search(pattern, page_content, re.IGNORECASE)
        if match:
            invoice_data[category][key] = match.group(1).strip()

    # Use NLP to detect customer name and company name
    doc = nlp(page_content)

    for ent in doc.ents:
        if ent.label_ == "ORG" and "company_name" not in invoice_data["billing_info"]:
            invoice_data["billing_info"]["company_name"] = ent.text
        elif ent.label_ == "PERSON":  # Extracts the correct customer name
            if "customer_name" not in invoice_data["billing_info"] or len(ent.text) > len(
                invoice_data["billing_info"].get("customer_name", "")
            ):
                invoice_data["billing_info"]["customer_name"] = ent.text

# Convert extracted data to JSON
json_output = json.dumps(invoice_data, indent=4)
print(json_output)

# Save output to JSON file
with open("categorized_invoice_data.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_output)

import spacy

# Load spaCy model once when the module is imported
nlp = spacy.load("en_core_web_sm")

def run_spacy(extracted_text: str) -> dict:
    
    if not extracted_text or not isinstance(extracted_text, str):
        return {}

    entities = {}

    # Process the entire text as one document
    doc = nlp(extracted_text)

    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = ent.text
        elif isinstance(entities[ent.label_], list):
            entities[ent.label_].append(ent.text)
        else:
            entities[ent.label_] = [entities[ent.label_], ent.text]

    return entities
"""