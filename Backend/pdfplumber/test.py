import os
import mimetypes
import pdfplumber
import json
import csv
import pandas as pd
from docx import Document
import re


def clean_text(text):
    """Clean text by removing excessive whitespace and line breaks."""
    return " ".join(text.split()) if text else None


def decode_unicode_escape_sequences(text):
    """Decode Unicode escape sequences in the given text."""
    escape_sequence_pattern = r'\\u[0-9A-Fa-f]{4}|\\U[0-9A-Fa-f]{8}|\\[0-7]{1,3}|\\x[0-9A-Fa-f]{2}'

    def replace_match(match):
        escape_sequence = match.group(0)
        return bytes(escape_sequence, "utf-8").decode("unicode_escape")

    decoded_text = re.sub(escape_sequence_pattern, replace_match, text)
    return decoded_text


def extract_and_map_table(page):
    """Extract tables from the page and map data to their corresponding headings."""
    tables = page.extract_tables()
    mapped_tables = []

    for table in tables:
        if table and len(table) > 1:  # Ensure the table has a header and rows
            headers = [clean_text(cell) for cell in table[0]]  # First row as headers
            for row in table[1:]:
                mapped_row = {headers[i]: clean_text(cell) for i, cell in enumerate(row) if i < len(headers)}
                mapped_tables.append(mapped_row)
    return mapped_tables


def extract_images_from_pdf(file_path, output_dir="extracted_images"):
    """Extract images from a PDF and save them as separate files."""
    os.makedirs(output_dir, exist_ok=True)
    image_paths = []

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for i, img_obj in enumerate(page.images):
                # Extract image bounding box coordinates
                x0, top, x1, bottom = img_obj["x0"], img_obj["top"], img_obj["x1"], img_obj["bottom"]
                cropped_image = page.crop((x0, top, x1, bottom)).to_image()
                output_file = os.path.join(output_dir, f"page_{page_number}_image_{i + 1}.png")
                cropped_image.save(output_file)
                image_paths.append(output_file)

    return image_paths


def process_pdf(file_path):
    """Process a PDF file to extract text, tables, and images."""
    pdf_data = {"file_type": "PDF", "pages": []}
    plain_text_pages = []
    images = extract_images_from_pdf(file_path)

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_data = {"page_number": page_number, "text": None, "tables": []}
            text = page.extract_text()
            if text:
                cleaned_text = clean_text(text)
                decoded_text = decode_unicode_escape_sequences(cleaned_text)
                page_data["text"] = decoded_text
                plain_text_pages.append(f"Page {page_number}:\n{decoded_text}\n")

            # Extract and map tables for JSON output
            tables = extract_and_map_table(page)
            if tables:
                page_data["tables"].extend(tables)

            pdf_data["pages"].append(page_data)

    pdf_data["txt_content"] = "\n".join(plain_text_pages)  # Combine text for JSON
    pdf_data["images"] = images  # Include the extracted images
    return pdf_data, plain_text_pages


def process_txt(file_path):
    """Process a plain text file."""
    with open(file_path, "r", encoding="utf-8") as txt_file:
        text = txt_file.read()
    cleaned_text = clean_text(text)
    decoded_text = decode_unicode_escape_sequences(cleaned_text)
    return {"file_type": "TXT", "content": decoded_text, "txt_content": decoded_text}


def process_file(file_path):
    """Determine the file format and process it."""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type == "application/pdf":
        return process_pdf(file_path)
    elif mime_type == "text/plain":
        return process_txt(file_path), []
    else:
        return {"error": f"Unsupported file type: {mime_type}"}, []


def main():
    file_path = input("Enter the file path: ")
    if os.path.exists(file_path):
        data, plain_text_pages = process_file(file_path)

        if "error" in data:
            print(data["error"])
            return

        # Save as JSON
        json_output = json.dumps(data, indent=4, ensure_ascii=False)
        output_file_json = "output.json"
        with open(output_file_json, "w", encoding="utf-8") as json_file:
            json_file.write(json_output)
        print(f"JSON output saved to {output_file_json}")

        # Save plain text content
        output_file_txt = "output.txt"
        if plain_text_pages:
            with open(output_file_txt, "w", encoding="utf-8") as txt_file:
                txt_file.write("\n".join(plain_text_pages))
            print(f"Text output saved to {output_file_txt}")

        # Display extracted images
        print("Extracted images saved in the 'extracted_images' directory.")
    else:
        print("File not found. Please provide a valid file path.")


if __name__ == "__main__":
    main()
